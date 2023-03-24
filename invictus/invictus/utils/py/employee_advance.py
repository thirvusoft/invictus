import frappe


@frappe.whitelist()
def employee_adv_status_update(doc, event=None):
    linked_doc = frappe.db.get_all('Travel Request Advance', filters={'advance':doc.name}, pluck='name')
    for i in linked_doc:
        frappe.db.set_value('Travel Request Advance', i, 'status', doc.status)