from . import __version__ as app_version

app_name = "invictus"
app_title = "Invictus"
app_publisher = "Thirvusoft"
app_description = "Travel Management"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "thirvusoft@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/invictus/css/invictus.css"
# app_include_js = "/assets/invictus/js/invictus.js"

# include js, css files in header of web template
# web_include_css = "/assets/invictus/css/invictus.css"
# web_include_js = "/assets/invictus/js/invictus.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "invictus/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Travel Request" : "utils/js/travel_request.js",
              "Expense Claim":"utils/js/expense_claim.js",
            #   "Travel Request":"utils/js/travel_request_costings.js"
              }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# boot_session = "invictus.utils.py.session_defaults.session_defaults"
after_install = "invictus.install.after_install"


# Migration
#-------------

# after_migrate = "invictus.install.after_install"
# Uninstallation
# ------------

# before_uninstall = "invictus.uninstall.before_uninstall"
# after_uninstall = "invictus.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "invictus.notifications.get_notification_config"

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

doc_events = {
	"Travel Request": {
		"on_update_after_submit": ["invictus.utils.py.employee_advance.employee_advance",
                             "invictus.utils.py.travel_request.totals"],
		"after_insert":"invictus.utils.py.travel_request.costing_details",
		"validate":["invictus.utils.py.travel_request.send_emails",
              "invictus.utils.py.travel_request.costing_details",
              "invictus.utils.py.travel_request.eligibal_amount"
              ],
		"on_submit":["invictus.utils.py.travel_request.travel_approve"],
		"onload":"invictus.utils.py.travel_request.status_update"

	},
 
 	"Employee Advance": {
		"on_submit":"invictus.utils.py.employee_advance.status_change"

	},
  	"Employee":{
		"validate":["invictus.utils.py.user_permission.user_permission",
              "invictus.utils.py.user_permission.user_permission_employee"]

	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"invictus.tasks.all"
# 	],
# 	"daily": [
# 		"invictus.tasks.daily"
# 	],
# 	"hourly": [
# 		"invictus.tasks.hourly"
# 	],
# 	"weekly": [
# 		"invictus.tasks.weekly"
# 	]
# 	"monthly": [
# 		"invictus.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "invictus.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "invictus.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "invictus.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"invictus.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
