import frappe

@frappe.whitelist()
def add_comment(doc, comment='', action=''):
    doc = frappe.get_doc('Travel Request', doc)
    comment = f"<p>{action} Reason:</p>"+comment
    doc.add_comment('Comment',comment)

@frappe.whitelist()
def get_meta(doc="Employee Advance"):
    return frappe.get_meta(doc)

@frappe.whitelist()
def create_employee_advance(data):
	if isinstance(data, str):
		import json
		data = json.loads(data)
	adv = frappe.new_doc('Employee Advance')
	adv.update(data)
	adv.flags.ignore_mandatory = True
	adv.flags.ignore_permissions = True
	adv.insert()
	tr = frappe.get_doc('Travel Request', data['travel_request'])
	tr.append('travel_request_advance', {'advance':adv.name, 'amount':data['advance_amount']})
	tr.save()
	return adv

@frappe.whitelist()
def submit_employee_advance(emp_adv):
	adv = frappe.get_doc('Employee Advance', emp_adv)
	adv.flags.ignore_mandatory = True
	adv.flags.ignore_permissions = True
	adv.submit()