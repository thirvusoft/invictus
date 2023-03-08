import frappe

def after_install():
    create_mode_of_transports()
    
def create_mode_of_transports():
    mot = frappe.new_doc('Mode of Transport Class')
    if(not frappe.db.exists('Mode of Transport Class', 'Air')):
        mot.update({
            'mode_of_transport':'Air',
            'is_group':1
        })
        mot.insert()
    mot = frappe.new_doc('Mode of Transport Class')
    if(not frappe.db.exists('Mode of Transport Class', 'Road')):
        mot.update({
            'mode_of_transport':'Road',
            'is_group':1
        })
        mot.insert()
    mot = frappe.new_doc('Mode of Transport Class')
    if(not frappe.db.exists('Mode of Transport Class', 'Rail')):
        mot.update({
            'mode_of_transport':'Rail',
            'is_group':1
        })
        mot.insert()