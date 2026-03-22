# Copyright (c) 2026, lakshmir and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document

class BrokenItemRegister(Document):
    def on_submit(self):
        # 1. Create the Stock Entry
        stock_entry = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Issue",
            "posting_date": self.broken_date,
            "from_warehouse": self.lab_location,
            "custom_register_volume": self.register_volume,
            "custom_register_page": self.register_page,
            "items": [{
                "item_code": self.item_name,       #
                "qty": self.quantity_broken,       #
                "s_warehouse": self.lab_location,  #
                "uom": frappe.db.get_value("Item", self.item_name, "stock_uom")
            }],
            "remarks": f"Breakage: {self.name}"
        })
        
        # 2. Submit the Stock Entry
        stock_entry.insert(ignore_permissions=True)
        stock_entry.submit()
        
        # 3. Save the link back to this document
        self.db_set("stock_entry_linkage", stock_entry.name)
        
        frappe.msgprint(f"Stock Entry {stock_entry.name} created and linked.")