import frappe
from frappe import _
from frappe.utils import flt
from frappe import _dict

from erpnext.stock.report.stock_balance.stock_balance import execute



@frappe.whitelist()
def get_stock_dashboard_data(
    financial_year=None,
    laboratory=None
):

    # =====================================================
    # GET FINANCIAL YEAR DATES
    # =====================================================

    from_date = None
    to_date = None

    if financial_year:

        fy = frappe.db.get_value(
            "Fiscal Year",
            financial_year,
            ["year_start_date", "year_end_date"],
            as_dict=True
        )

        if fy:
            from_date = fy.year_start_date
            to_date = fy.year_end_date



    # =====================================================
    # STOCK BALANCE FILTERS
    # =====================================================

    filters = _dict({
        "company":
            "Soil Survey and Soil Conservation Department"
    })



    # =====================================================
    # APPLY DATE FILTER ONLY IF FY SELECTED
    # =====================================================

    if from_date and to_date:

        filters.from_date = from_date
        filters.to_date = to_date



    # =====================================================
    # INCLUDE ZERO STOCK ITEMS
    # ONLY WHEN NO FILTERS
    # =====================================================

    if not financial_year and not laboratory:

        filters.include_zero_stock_items = 1



    # =====================================================
    # LABORATORY FILTER
    # =====================================================

    if laboratory:

        filters.warehouse = laboratory



    # =====================================================
    # GET STOCK BALANCE REPORT
    # =====================================================

    columns, data = execute(filters)



    # =====================================================
    # TOTAL STOCK VALUE
    # AVAILABLE QTY
    # =====================================================

    total_stock_value = 0
    available_qty = 0

    for row in data:

        bal_qty = flt(row.get("bal_qty"))
        bal_val = flt(row.get("bal_val"))

        # IGNORE ZERO STOCK ROWS
        if bal_qty > 0:

            total_stock_value += bal_val
            available_qty += bal_qty



    # =====================================================
    # PURCHASE VALUE
    # ONLY STOCK ITEMS
    # =====================================================

    purchase_conditions = [
        "pr.docstatus = 1",
        "IFNULL(pri.custom_is_stock_item,0)=1"
    ]



    # =====================================================
    # LAB FILTER
    # =====================================================

    if laboratory:

        purchase_conditions.append(
            "pri.warehouse = %(laboratory)s"
        )



    # =====================================================
    # FY FILTER
    # =====================================================

    if from_date and to_date:

        purchase_conditions.append(
            """
            pr.posting_date
            BETWEEN %(from_date)s
            AND %(to_date)s
            """
        )



    purchase_where = " AND ".join(
        purchase_conditions
    )



    purchase_value = frappe.db.sql(f"""

        SELECT
            IFNULL(SUM(pri.base_amount),0)

        FROM `tabPurchase Receipt Item` pri

        INNER JOIN `tabPurchase Receipt` pr
            ON pr.name = pri.parent

        WHERE {purchase_where}

    """, {
        "laboratory": laboratory,
        "from_date": from_date,
        "to_date": to_date
    })[0][0] or 0



    # =====================================================
    # MATERIAL ISSUES
    # =====================================================

    issue_conditions = [
        "docstatus = 1",
        "stock_entry_type = 'Material Issue'",
        "IFNULL(custom_is_broken_item_entry,0)=0"
    ]



    if laboratory:

        issue_conditions.append(
            "from_warehouse = %(laboratory)s"
        )



    if from_date and to_date:

        issue_conditions.append(
            """
            posting_date
            BETWEEN %(from_date)s
            AND %(to_date)s
            """
        )



    issue_where = " AND ".join(
        issue_conditions
    )



    material_issues = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabStock Entry`

        WHERE {issue_where}

    """, {
        "laboratory": laboratory,
        "from_date": from_date,
        "to_date": to_date
    })[0][0] or 0



    # =====================================================
    # MATERIAL TRANSFERS
    # =====================================================

    transfer_conditions = [
        "docstatus = 1",
        "stock_entry_type = 'Material Transfer'"
    ]



    if laboratory:

        transfer_conditions.append(
            "from_warehouse = %(laboratory)s"
        )



    if from_date and to_date:

        transfer_conditions.append(
            """
            posting_date
            BETWEEN %(from_date)s
            AND %(to_date)s
            """
        )



    transfer_where = " AND ".join(
        transfer_conditions
    )



    transfers = frappe.db.sql(f"""

        SELECT COUNT(name)

        FROM `tabStock Entry`

        WHERE {transfer_where}

    """, {
        "laboratory": laboratory,
        "from_date": from_date,
        "to_date": to_date
    })[0][0] or 0



    # =====================================================
    # DAMAGED ITEMS
    # FROM BROKEN ITEM REGISTER
    # =====================================================

    damage_conditions = [
        "docstatus =1"
    ]



    if laboratory:

        damage_conditions.append(
            "lab_location = %(laboratory)s"
        )



    if from_date and to_date:

        damage_conditions.append(
            """
            broken_date
            BETWEEN %(from_date)s
            AND %(to_date)s
            """
        )



    damage_where = " AND ".join(
        damage_conditions
    )



    damaged_items = frappe.db.sql(f"""

        SELECT IFNULL(SUM(quantity_broken),0)

        FROM `tabBroken Item Register`

        WHERE {damage_where}

    """, {
        "laboratory": laboratory,
        "from_date": from_date,
        "to_date": to_date
    })[0][0] or 0



    # =====================================================
    # RETURN
    # =====================================================

    return {

        "total_stock_value":
            flt(total_stock_value),

        "available_qty":
            flt(available_qty),

        "purchase_value":
            flt(purchase_value),

        "material_issues":
            material_issues,

        "transfers":
            transfers,

        "damaged_items":
            damaged_items
    }







#purchase receipt graph 
@frappe.whitelist()
def get_purchase_receipt_trends(
    financial_year=None,
    laboratory=None,
    trend_type="Monthly"
):

    from frappe.utils import flt

    from_date = None
    to_date = None



    # =====================================================
    # FINANCIAL YEAR
    # =====================================================

    if financial_year:

        fy = frappe.db.get_value(
            "Fiscal Year",
            financial_year,
            ["year_start_date", "year_end_date"],
            as_dict=True
        )

        if fy:

            from_date = fy.year_start_date
            to_date = fy.year_end_date



    # =====================================================
    # CONDITIONS
    # =====================================================

    conditions = [
        "pr.docstatus = 1",
        "IFNULL(pri.custom_is_stock_item,0)=1"
    ]



    if laboratory:

        conditions.append(
            "pr.set_warehouse = %(laboratory)s"
        )



    if from_date and to_date:

        conditions.append(
            """
            pr.custom_purchased_date
            BETWEEN %(from_date)s
            AND %(to_date)s
            """
        )



    where_clause = " AND ".join(conditions)



    # =====================================================
    # GROUPING
    # =====================================================

    if trend_type == "Quarterly":

        select_field = """

            CONCAT(
                'Q',
                QUARTER(pr.custom_purchased_date)
            ) as label

        """

        group_by = """
            QUARTER(pr.custom_purchased_date)
        """

        order_by = """
            QUARTER(pr.custom_purchased_date)
        """



    elif trend_type == "Yearly":

        select_field = """

            YEAR(
                pr.custom_purchased_date
            ) as label

        """

        group_by = """
            YEAR(pr.custom_purchased_date)
        """

        order_by = """
            YEAR(pr.custom_purchased_date)
        """



    else:

        select_field = """

            MONTHNAME(
                pr.custom_purchased_date
            ) as label

        """

        group_by = """
            MONTH(pr.custom_purchased_date)
        """

        order_by = """
            MONTH(pr.custom_purchased_date)
        """



    # =====================================================
    # QUERY
    # =====================================================

    data = frappe.db.sql(f"""

        SELECT

            {select_field},

            SUM(pri.base_amount)
                as purchase_value

        FROM `tabPurchase Receipt` pr

        INNER JOIN
            `tabPurchase Receipt Item` pri

            ON pri.parent = pr.name

        WHERE {where_clause}

        GROUP BY {group_by}

        ORDER BY {order_by}

    """, {

        "laboratory": laboratory,

        "from_date": from_date,

        "to_date": to_date

    }, as_dict=True)



    labels = []
    values = []



    for row in data:

        labels.append(row.label)

        values.append(
            flt(row.purchase_value)
        )



    return {

        "labels": labels,

        "values": values

    }

#employee wise dashboard stock
import frappe

from frappe import _dict
from frappe.utils import flt

from erpnext.stock.report.stock_balance.stock_balance import execute



# =========================================================
# EMPLOYEE STOCK DASHBOARD
# =========================================================

@frappe.whitelist()
def get_employee_stock_dashboard(financial_year=None):

    user = frappe.session.user



    # =====================================================
    # USER WAREHOUSE
    # =====================================================

    allowed_warehouses = frappe.get_all(

        "User Permission",

        filters={

            "user": user,

            "allow": "Warehouse"

        },

        fields=["for_value"]

    )



    warehouse_list = [

        d.for_value
        for d in allowed_warehouses

    ]



    # =====================================================
    # NO ACCESS
    # =====================================================

    if not warehouse_list:

        return {

            "total_stock_value": 0,

            "available_qty": 0,

            "purchase_value": 0,

            "material_issues": 0,

            "transfers": 0,

            "damaged_items": 0

        }



    # =====================================================
    # FY DATES
    # =====================================================

    from_date = None
    to_date = None



    if financial_year:

        fy = frappe.db.get_value(

            "Fiscal Year",

            financial_year,

            [

                "year_start_date",
                "year_end_date"

            ],

            as_dict=True

        )



        if fy:

            from_date = fy.year_start_date
            to_date = fy.year_end_date



    # =====================================================
    # STOCK BALANCE
    # =====================================================

    filters = _dict({

        "company":
            "Soil Survey and Soil Conservation Department",

        "warehouse":
            warehouse_list[0]

    })



    if from_date and to_date:

        filters.from_date = from_date
        filters.to_date = to_date



    columns, data = execute(filters)



    total_stock_value = 0
    available_qty = 0



    for row in data:

        bal_qty = flt(
            row.get("bal_qty")
        )



        bal_val = flt(
            row.get("bal_val")
        )



        if bal_qty > 0:

            total_stock_value += bal_val
            available_qty += bal_qty



    # =====================================================
    # PURCHASE VALUE
    # =====================================================

    purchase_value = frappe.db.sql("""

        SELECT

            IFNULL(
                SUM(pri.base_amount),
                0
            )

        FROM `tabPurchase Receipt Item` pri

        INNER JOIN `tabPurchase Receipt` pr
            ON pr.name = pri.parent

        WHERE pr.docstatus = 1

        AND pri.warehouse = %(warehouse)s

    """, {

        "warehouse":
            warehouse_list[0]

    })[0][0] or 0



    # =====================================================
    # MATERIAL ISSUES
    # =====================================================

    material_issues = frappe.db.count(

        "Stock Entry",

        {

            "docstatus":1,

            "stock_entry_type":
                "Material Issue",

            "from_warehouse":
                warehouse_list[0]

        }

    )



    # =====================================================
    # TRANSFERS
    # =====================================================

    transfers = frappe.db.count(

        "Stock Entry",

        {

            "docstatus":1,

            "stock_entry_type":
                "Material Transfer",

            "from_warehouse":
                warehouse_list[0]

        }

    )



    # =====================================================
    # DAMAGED ITEMS
    # =====================================================

    damaged_items = frappe.db.sql("""

        SELECT

            IFNULL(
                SUM(quantity_broken),
                0
            )

        FROM `tabBroken Item Register`

        WHERE lab_location = %(warehouse)s

    """, {

        "warehouse":
            warehouse_list[0]

    })[0][0] or 0



    return {

        "total_stock_value":
            flt(total_stock_value),

        "available_qty":
            flt(available_qty),

        "purchase_value":
            flt(purchase_value),

        "material_issues":
            material_issues,

        "transfers":
            transfers,

        "damaged_items":
            damaged_items

    }





# =========================================================
# STOCK GROUP DISTRIBUTION
# =========================================================

@frappe.whitelist()
def get_stock_group_distribution():

    user = frappe.session.user



    # =====================================================
    # USER WAREHOUSE
    # =====================================================

    allowed_warehouses = frappe.get_all(

        "User Permission",

        filters={

            "user": user,

            "allow": "Warehouse"

        },

        fields=["for_value"]

    )



    warehouse_list = [

        d.for_value
        for d in allowed_warehouses

    ]



    # =====================================================
    # NO ACCESS
    # =====================================================

    if not warehouse_list:

        return {

            "labs": [],

            "groups": []

        }



    # =====================================================
    # LAB NAMES
    # =====================================================

    lab_names = []



    for warehouse in warehouse_list:

        clean_name = warehouse.split(" - ")[0]



        if clean_name not in lab_names:

            lab_names.append(clean_name)



    # =====================================================
    # ITEM GROUP DISTRIBUTION
    # =====================================================

    groups = frappe.db.sql("""

        SELECT

            ig.name as item_group,

            COUNT(i.name) as qty

        FROM `tabItem Group` ig

        INNER JOIN `tabItem Default` id
            ON id.parent = ig.name

        LEFT JOIN `tabItem` i
            ON i.item_group = ig.name

        WHERE id.default_warehouse IN %(warehouses)s

        GROUP BY ig.name

        ORDER BY qty DESC

    """, {

        "warehouses":
            tuple(warehouse_list)

    }, as_dict=1)



    return {

        "labs":
            lab_names,

        "groups":
            groups

    }