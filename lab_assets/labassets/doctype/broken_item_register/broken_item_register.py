import frappe
from frappe.model.document import Document


class BrokenItemRegister(Document):

    def on_submit(self):

        # =====================================
        # CREATE STOCK ENTRY
        # =====================================

        stock_entry = frappe.get_doc({

            "doctype": "Stock Entry",

            "stock_entry_type": "Material Issue",

            "posting_date": self.broken_date,

            "from_warehouse": self.lab_location,

            "custom_register_volume": self.register_volume,

            "custom_register_page": self.register_page,

            # =====================================
            # THIS FIELD BELONGS TO STOCK ENTRY
            # =====================================

            "custom_is_broken_item_entry": 1,

            "items": [{

                "item_code": self.item_name,

                "qty": self.quantity_broken,

                "s_warehouse": self.lab_location,

                "uom": frappe.db.get_value(

                    "Item",

                    self.item_name,

                    "stock_uom"

                )

            }],

            "remarks": f"Breakage: {self.name}"

        })


        # =====================================
        # INSERT STOCK ENTRY
        # =====================================

        stock_entry.insert(
            ignore_permissions=True
        )


        # =====================================
        # SUBMIT STOCK ENTRY
        # =====================================

        stock_entry.submit()


        # =====================================
        # SAVE LINK BACK
        # =====================================

        self.db_set(

            "stock_entry_linkage",

            stock_entry.name

        )


        frappe.msgprint(

            f"Stock Entry {stock_entry.name} created and linked."

        )