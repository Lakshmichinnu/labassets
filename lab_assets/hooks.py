app_name = "lab_assets"
app_title = "labassets"
app_publisher = "lakshmir"
app_description = "Assets for lab"
app_email = "lakshmir@icfoss.org"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "lab_assets",
# 		"logo": "/assets/lab_assets/logo.png",
# 		"title": "labassets",
# 		"route": "/lab_assets",
# 		"has_permission": "lab_assets.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/lab_assets/css/lab_assets.css"
#app_include_css = "/assets/lab_assets/css/custom.css"
# app_include_js = "/assets/lab_assets/js/lab_assets.js"
#app_include_js = "/assets/lab_assets/js/workspace_filters.js"

# include js, css files in header of web template
# web_include_css = "/assets/lab_assets/css/lab_assets.css"
# web_include_js = "/assets/lab_assets/js/lab_assets.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "lab_assets/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
doctype_list_js = {
    "Item": "public/js/item_list.js"
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "lab_assets/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "lab_assets.utils.jinja_methods",
# 	"filters": "lab_assets.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "lab_assets.install.before_install"
# after_install = "lab_assets.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "lab_assets.uninstall.before_uninstall"
# after_uninstall = "lab_assets.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "lab_assets.utils.before_app_install"
# after_app_install = "lab_assets.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "lab_assets.utils.before_app_uninstall"
# after_app_uninstall = "lab_assets.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lab_assets.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"lab_assets.tasks.all"
# 	],
# 	"daily": [
# 		"lab_assets.tasks.daily"
# 	],
# 	"hourly": [
# 		"lab_assets.tasks.hourly"
# 	],
# 	"weekly": [
# 		"lab_assets.tasks.weekly"
# 	],
# 	"monthly": [
# 		"lab_assets.tasks.monthly"
# 	],
# }
scheduler_events = {
    "daily": [
        "lab_assets.warranty_notification.send_warranty_expiry_notification",
        "lab_assets.amc_notification.send_amc_expiry_notification"
    ]
}

# Testing
# -------

# before_tests = "lab_assets.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "lab_assets.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "lab_assets.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["lab_assets.utils.before_request"]
# after_request = ["lab_assets.utils.after_request"]

# Job Events
# ----------
# before_job = ["lab_assets.utils.before_job"]
# after_job = ["lab_assets.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"lab_assets.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

fixtures = [

    # =====================================================
    # CUSTOM FIELD
    # =====================================================

    {
        "dt": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [

                    "Item-custom_lab",

                    "Asset-custom_register_page_number",
                    "Asset-custom_register_volume",
                    "Asset-custom_section_break_wmjiv",
                    "Asset-custom_amc_end_date",
                    "Asset-custom_amc_start_date",
                    "Asset-custom_warranty_end_date",
                    "Asset-custom_warranty_start_date",
                    "Asset-custom_section_break_bxvgc",
                    "Asset-custom_seral_no",
                    "Asset-custom_model_name",
                    "Asset-custom_section_break_cbnis",
                    "Asset-custom_brought_forward",
                    "Asset-custom_carry_over",
                    "Asset-custom_invoice_details",
                    "Asset-custom_amc_status",
                    "Asset-custom_warranty_status",

                    "Purchase Receipt-custom_page_number_of_register",
                    "Purchase Receipt-custom_purchase_invoice_number",
                    "Purchase Receipt-custom__register_volume",
                    "Purchase Receipt-custom_plan_fund",
                    "Purchase Receipt-custom_purchased_date",
                    "Purchase Receipt-custom_purchase_through",
                    "Purchase Indent-workflow_state",
                    "Purchase Receipt-custom_register_name",
                    "Purchase Receipt-custom_invoice",
                    "Purchase Receipt Item-custom_is_stock_item",

                    "Stock Entry-custom_register_name",
                    "Stock Entry-custom_register_page",
                    "Stock Entry-custom_register_volume",
                    "Stock Entry-custom_section_break_fcfqk",
                    "Stock Entry-custom_issued_employee",
                    "Stock Entry-custom_carried_over",
                    "Stock Entry-custom_brought_forward",
                    "Stock Entry-custom_received_from",
                    "Stock Entry-custom_issued_employee_name",
                    "Stock Entry-custom_is_broken_item_entry",
                    "Stock Entry-custom_remarks_for_issuing",


                    "Asset Maintenance-custom_register_page_",
                    "Asset Maintenance-custom_register_volume",
                    "Asset Maintenance-custom_section_break_ejq4u",
                    

                ]
            ]
        ]
    },

    # =====================================================
    # CLIENT SCRIPT
    # =====================================================

    {
        "dt": "Client Script",
        "filters": [
            [
                "name",
                "in",
                [

                    "asset_namin_series in asset doctype",
                    "itms in the respective login lab",
                    "Unserviceable or Damaged in asset navigation",
                    "hiding button in stock entry",
                    "asset naming series in item doctype with admin",
                    "hide purchase receipt create button inner options",
                    "hiding button in stock entry",


                ]
            ]
        ]
    },

    # =====================================================
    # WORKFLOW
    # =====================================================

    {
        "dt": "Workflow",
        "filters": [
            [
                "name",
                "in",
                [
                    "purchase indent",
                    "Unserviceable"
                ]
            ]
        ]
    },

    # =====================================================
    # PROPERTY SETTER
    # =====================================================

    {
        "dt": "Property Setter"
    },

    # =====================================================
    # SERVER SCRIPT
    # =====================================================

    {
        "dt": "Server Script",
        "filters": [
            [
                "name",
                "in",
                [
                    "status to scrapped in asset",
                    "Restore Asset from scrap when req delete",
                    "Automatic status update for AMC and Warranty"
                ]
            ]
        ]
    },

    # =====================================================
    # WORKFLOW STATE
    # =====================================================

    {
        "dt": "Workflow State"
    },

    # =====================================================
    # WORKSPACE
    # =====================================================

    {
        "dt": "Workspace",
        "filters": [
            [
                "module",
                "=",
                "labassets"
            ]
        ]
    },

    # =====================================================
    # CUSTOM HTML BLOCK
    # =====================================================

    {
        "dt": "Custom HTML Block",
        "filters": [
            [
                "name",
                "in",
                [
                    
                    "Asset Creation_Lab wise",
                    "Employewise_stock_dashboard",
                    "Stock operation_employee",
                    "Stock Purchase Trends",
                    "Lab-wise Asset Category Distribution",
                    "financial year selection",
                    "both employee_asset and chart",
                    "Stock Management Overview"
                ]
            ]
        ]
    },

    # =====================================================
    # DASHBOARD CHART
    # =====================================================

    {
        "dt": "Dashboard Chart",
        "filters": [
            [
                "module",
                "=",
                "labassets"
            ]
        ]
    },

   
]