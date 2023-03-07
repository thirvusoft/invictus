import frappe

@frappe.whitelist()
def add_comment(doc, comment='', action=''):
    doc = frappe.get_doc('Travel Request', doc)
    comment = f"<p>{action} Reason:</p>"+comment
    doc.add_comment('Comment',comment)