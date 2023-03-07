import frappe

def after_install():
    create_mode_of_transports()
    
def create_mode_of_transports():
    mot = frappe.new_doc('Mode of Transport')
    if(not frappe.db.exists('Mode of Transport', 'Air')):
        mot.update({
            'mode_of_transport':'Air',
            'is_group':1
        })
        mot.insert()
    mot = frappe.new_doc('Mode of Transport')
    if(not frappe.db.exists('Mode of Transport', 'Road')):
        mot.update({
            'mode_of_transport':'Road',
            'is_group':1
        })
        mot.insert()
    mot = frappe.new_doc('Mode of Transport')
    if(not frappe.db.exists('Mode of Transport', 'Rail')):
        mot.update({
            'mode_of_transport':'Rail',
            'is_group':1
        })
        mot.insert()