import frappe
from frappe.utils import nowdate, add_months, getdate

def send_warranty_expiry_notification():

    today = getdate(nowdate())
    reminder_date = add_months(today, 2)

    # Assets expiring in 2 months
    assets = frappe.get_all(
        "Asset",
        filters={"custom_warranty_end_date": reminder_date},
        fields=["name", "asset_name", "location"]
    )

    # Users with Senior Chemist role
    users = frappe.get_all(
        "Has Role",
        filters={
            "role": "Labs Asset Dashboard Viewer",
            "parenttype": "User"
        },
        pluck="parent"
    )

    for user in users:

        # Get location permission of user
        user_locations = frappe.get_all(
            "User Permission",
            filters={
                "user": user,
                "allow": "Location"
            },
            pluck="for_value"
        )

        if not user_locations:
            continue

        for asset in assets:

            if asset.location in user_locations:

                frappe.get_doc({
                    "doctype": "Notification Log",
                    "subject": f"Warranty Expiry Alert: {asset.asset_name}",
                    "for_user": user,
                    "type": "Alert",
                    "document_type": "Asset",
                    "document_name": asset.name
                }).insert(ignore_permissions=True)

    frappe.db.commit()