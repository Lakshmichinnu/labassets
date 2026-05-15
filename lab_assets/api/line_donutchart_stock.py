import frappe
from frappe.utils import flt



# =====================================================
# LINE CHART
# =====================================================

@frappe.whitelist()
def get_purchase_receipt_trends(
    financial_year=None,
    laboratory=None
):

    conditions = ""

    values = []



    if financial_year:

        fy = frappe.get_doc(
            "Fiscal Year",
            financial_year
        )

        conditions += """

            AND pr.posting_date
            BETWEEN %s AND %s

        """

        values.extend([
            fy.year_start_date,
            fy.year_end_date
        ])



    if laboratory:

        conditions += """

            AND pri.warehouse = %s

        """

        values.append(laboratory)



    data = frappe.db.sql("""

        SELECT

            DATE_FORMAT(
                pr.posting_date,
                '%%b %%Y'
            ) AS period,

            SUM(pri.amount) AS total

        FROM `tabPurchase Receipt` pr

        INNER JOIN
            `tabPurchase Receipt Item` pri
            ON pri.parent = pr.name

        WHERE

            pr.docstatus = 1

            AND IFNULL(
                pri.custom_is_stock_item,
                0
            ) = 1

            {conditions}

        GROUP BY
            YEAR(pr.posting_date),
            MONTH(pr.posting_date)

        ORDER BY
            pr.posting_date ASC

    """.format(
        conditions=conditions
    ), values, as_dict=True)



    return {

        "labels": [

            d.period
            for d in data

        ],

        "values": [

            flt(d.total)
            for d in data

        ]

    }





# =====================================================
# DONUT CHART
# =====================================================

@frappe.whitelist()
def get_purchase_source_chart(
    financial_year=None,
    laboratory=None
):

    conditions = ""

    values = []



    if financial_year:

        fy = frappe.get_doc(
            "Fiscal Year",
            financial_year
        )

        conditions += """

            AND pr.posting_date
            BETWEEN %s AND %s

        """

        values.extend([
            fy.year_start_date,
            fy.year_end_date
        ])



    if laboratory:

        conditions += """

            AND pri.warehouse = %s

        """

        values.append(laboratory)



    data = frappe.db.sql("""

        SELECT

            IFNULL(
                pr.custom_purchase_through,
                'Not Set'
            ) AS purchase_through,

            SUM(pri.amount) AS total

        FROM `tabPurchase Receipt` pr

        INNER JOIN
            `tabPurchase Receipt Item` pri
            ON pri.parent = pr.name

        WHERE

            pr.docstatus = 1

            AND IFNULL(
                pri.custom_is_stock_item,
                0
            ) = 1

            {conditions}

        GROUP BY
            pr.custom_purchase_through

        ORDER BY
            total DESC

    """.format(
        conditions=conditions
    ), values, as_dict=True)



    return {

        "labels": [

            d.purchase_through
            for d in data

        ],

        "values": [

            flt(d.total)
            for d in data

        ]

    }