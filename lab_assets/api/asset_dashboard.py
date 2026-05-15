import frappe
from frappe.utils import flt


@frappe.whitelist()
def get_dashboard_data(
    fiscal_year=None,
    laboratory=None
):

    # ==================================================
    # FY FILTER
    # ==================================================

    fy_condition = ""

    fy_values = {}



    if fiscal_year:

        fy = frappe.get_doc(
            "Fiscal Year",
            fiscal_year
        )

        fy_condition = """

            AND purchase_date
            BETWEEN %(from_date)s
            AND %(to_date)s

        """

        fy_values = {

            "from_date":
                fy.year_start_date,

            "to_date":
                fy.year_end_date

        }



    # ==================================================
    # LAB FILTER
    # ==================================================

    lab_condition = ""



    if laboratory:

        lab_condition = """

            AND location = %(laboratory)s

        """



    # ==================================================
    # SQL VALUES
    # ==================================================

    sql_values = {

        **fy_values,

        "laboratory":
            laboratory

    }



    # ==================================================
    # TOTAL ASSETS
    # ==================================================

    total_assets = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabAsset`

        WHERE docstatus < 2

        {lab_condition}

        {fy_condition}

    """, sql_values)[0][0] or 0



    # ==================================================
    # PURCHASE VALUE
    # ==================================================

    purchase_value = frappe.db.sql(f"""

        SELECT SUM(gross_purchase_amount)

        FROM `tabAsset`

        WHERE docstatus < 2

        {lab_condition}

        {fy_condition}

    """, sql_values)[0][0] or 0



    # ==================================================
    # ACTIVE ASSETS
    # ==================================================

    active_assets = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabAsset`

        WHERE docstatus = 1

        AND status != 'Scrapped'

        {lab_condition}

        {fy_condition}

    """, sql_values)[0][0] or 0



    # ==================================================
    # SCRAPPED
    # ==================================================

    scrapped_assets = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabAsset`

        WHERE status = 'Scrapped'

        {lab_condition}

        {fy_condition}

    """, sql_values)[0][0] or 0



    # ==================================================
    # AMC EXPIRED
    # ==================================================

    amc_expired = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabAsset`

        WHERE custom_amc_status = 'Expired'

        {lab_condition}

        {fy_condition}

    """, sql_values)[0][0] or 0



    # ==================================================
    # WARRANTY EXPIRED
    # ==================================================

    warranty_expired = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabAsset`

        WHERE custom_warranty_status = 'Expired'

        {lab_condition}

        {fy_condition}

    """, sql_values)[0][0] or 0



    # ==================================================
    # AMC EXPIRING SOON
    # ==================================================

    amc_expiring_soon = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabAsset`

        WHERE custom_amc_status = 'Expiring Soon'

        {lab_condition}

        {fy_condition}

    """, sql_values)[0][0] or 0



    # ==================================================
    # WARRANTY EXPIRING SOON
    # ==================================================

    warranty_expiring_soon = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabAsset`

        WHERE custom_warranty_status = 'Expiring Soon'

        {lab_condition}

        {fy_condition}

    """, sql_values)[0][0] or 0



    # ==================================================
    # UNDER REPAIR
    # ==================================================

    under_repair = frappe.db.sql(f"""

        SELECT COUNT(ar.name)

        FROM `tabAsset Repair` ar

        LEFT JOIN `tabAsset` a
        ON ar.asset = a.name

        WHERE ar.repair_status = 'Pending'

        {

            "AND a.location = %(laboratory)s"

            if laboratory else ""

        }

        {

            '''

            AND a.purchase_date
            BETWEEN %(from_date)s
            AND %(to_date)s

            '''

            if fiscal_year else ""

        }

    """, sql_values)[0][0] or 0



    # ==================================================
    # RETURN
    # ==================================================

    return {

        "total_assets":
            total_assets,

        "purchase_value":
            flt(purchase_value),

        "active_assets":
            active_assets,

        "under_repair":
            under_repair,

        "scrapped_assets":
            scrapped_assets,

        "amc_expired":
            amc_expired,

        "warranty_expired":
            warranty_expired,

        "amc_expiring_soon":
            amc_expiring_soon,

        "warranty_expiring_soon":
            warranty_expiring_soon

    }


#for employee dashboard 


@frappe.whitelist()
def get_employee_dashboard_data(
    fiscal_year=None
):

    user = frappe.session.user

    # =====================================================
    # USER LAB PERMISSION
    # =====================================================

    allowed_labs = frappe.get_all(

        "User Permission",

        filters={
            "user": user,
            "allow": "Soil Laboratory"
        },

        fields=["for_value"]

    )

    lab_names = [
        d.for_value
        for d in allowed_labs
    ]


    if not lab_names:

        return {

            "total_assets":0,
            "purchase_value":0,
            "active_assets":0,
            "under_repair":0,
            "scrapped_assets":0,
            "amc_expired":0,
            "warranty_expired":0

        }


    # =====================================================
    # FY CONDITION
    # =====================================================

    fy_condition = ""

    sql_values = {

        "labs":
            tuple(lab_names)

    }


    if fiscal_year:

        fy = frappe.get_doc(
            "Fiscal Year",
            fiscal_year
        )

        fy_condition = """

            AND purchase_date
            BETWEEN %(from_date)s
            AND %(to_date)s

        """

        sql_values["from_date"] = fy.year_start_date
        sql_values["to_date"] = fy.year_end_date


    # =====================================================
    # TOTAL ASSETS
    # =====================================================

    total_assets = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabAsset`

        WHERE location IN %(labs)s

        {fy_condition}

    """, sql_values)[0][0] or 0


    # =====================================================
    # PURCHASE VALUE
    # =====================================================

    purchase_value = frappe.db.sql(f"""

        SELECT SUM(gross_purchase_amount)

        FROM `tabAsset`

        WHERE location IN %(labs)s

        {fy_condition}

    """, sql_values)[0][0] or 0


    # =====================================================
    # ACTIVE
    # =====================================================

    active_assets = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabAsset`

        WHERE status != 'Scrapped'

        AND location IN %(labs)s

        {fy_condition}

    """, sql_values)[0][0] or 0


    # =====================================================
    # SCRAPPED
    # =====================================================

    scrapped_assets = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabAsset`

        WHERE status = 'Scrapped'

        AND location IN %(labs)s

        {fy_condition}

    """, sql_values)[0][0] or 0


    # =====================================================
    # AMC EXPIRED
    # =====================================================

    amc_expired = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabAsset`

        WHERE custom_amc_status = 'Expired'

        AND location IN %(labs)s

        {fy_condition}

    """, sql_values)[0][0] or 0


    # =====================================================
    # WARRANTY EXPIRED
    # =====================================================

    warranty_expired = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabAsset`

        WHERE custom_warranty_status = 'Expired'

        AND location IN %(labs)s

        {fy_condition}

    """, sql_values)[0][0] or 0


    # =====================================================
    # UNDER REPAIR
    # =====================================================

    under_repair = frappe.db.sql("""

        SELECT COUNT(ar.name)

        FROM `tabAsset Repair` ar

        LEFT JOIN `tabAsset` a
        ON ar.asset = a.name

        WHERE ar.repair_status = 'Pending'

        AND a.location IN %(labs)s

    """, sql_values)[0][0] or 0


    return {

        "total_assets":
            total_assets,

        "purchase_value":
            flt(purchase_value),

        "active_assets":
            active_assets,

        "under_repair":
            under_repair,

        "scrapped_assets":
            scrapped_assets,

        "amc_expired":
            amc_expired,

        "warranty_expired":
            warranty_expired

    }


#employee wise asset category distribution

@frappe.whitelist()
def get_asset_category_summary():

    user = frappe.session.user


    # =====================================================
    # GET USER LABS
    # =====================================================

    allowed_labs = frappe.get_all(

        "User Permission",

        filters={

            "user": user,

            "allow": "Soil Laboratory"

        },

        fields=["for_value"]

    )


    lab_names = [

        d.for_value
        for d in allowed_labs

    ]


    # =====================================================
    # NO LAB ACCESS
    # =====================================================

    if not lab_names:

        return {

            "labs": [],

            "categories": []

        }


    # =====================================================
    # CATEGORY SUMMARY
    # =====================================================

    categories = frappe.db.sql("""

        SELECT

            asset_category,

            COUNT(name) as count

        FROM `tabAsset`

        WHERE location IN %(labs)s

        GROUP BY asset_category

        ORDER BY count DESC

    """, {

        "labs": tuple(lab_names)

    }, as_dict=1)


    # =====================================================
    # RETURN
    # =====================================================

    return {

        "labs":
            lab_names,

        "categories":
            categories

    }