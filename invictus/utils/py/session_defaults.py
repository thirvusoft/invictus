import frappe

def session_defaults(self):
    employee =False
    session_settings=frappe.get_single('Session Default Settings')
    for i in session_settings.session_defaults:
        if i.ref_doctype=="Employee":
            employee=True
    if employee==False:
        session_settings.update({
            "session_defaults":session_settings.session_defaults+[{
                "ref_doctype":"Employee"
            }]
        })
    session_settings.save()
    employee=frappe.get_value('Employee',{'user_id':frappe.session.user},'name')
    frappe.defaults.set_user_default("employee",employee)