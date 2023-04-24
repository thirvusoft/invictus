import frappe 

def user_permission(doc,event):
    if not frappe.get_all("User Permission",{'user': doc.user_id, 'allow': "User", "for_value": doc.user_id, "apply_to_all_doctypes": 1,'is_default':1}):
        doc1=frappe.get_doc({
        'doctype':'User Permission',
        'user': doc.user_id, 
        'allow': "User", 
        "for_value": doc.user_id, 
        "apply_to_all_doctypes": 1,
        'is_default':1
        })
        doc1.flags.ignore_mandatory=True
        doc1.flags.ignore_permissions=True
        doc1.save()