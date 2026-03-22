# Copyright (c) 2026, lakshmir and contributors
# For license information, please see license.txt

# import frappe


import frappe

def execute(filters=None):

    data = frappe.db.sql("""
        SELECT
            location,
            SUM(gross_purchase_amount) as asset_value
        FROM
            `tabAsset`
        WHERE
            docstatus < 2
        GROUP BY
            location
        ORDER BY
            location
    """, as_dict=True)

    columns = [
        {
            "label": "Location",
            "fieldname": "location",
            "fieldtype": "Link",
            "options": "Location",
            "width": 200
        },
        {
            "label": "Asset Value",
            "fieldname": "asset_value",
            "fieldtype": "Currency",
            "width": 200
        }
    ]

    return columns, data