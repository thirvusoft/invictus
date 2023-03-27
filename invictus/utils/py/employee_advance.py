import frappe

def employee_advance(self,event):
    for i in self.travel_request_advance:
        if i.amount:
            new_employee_advance = frappe.new_doc("Employee Advance")
            new_employee_advance.update({
                "employee":self.employee,
                "travel_request":self.name,
                "purpose":self.purpose_of_travel,
                "advance_amount":i.amount,
                "advance_account":frappe.db.get_single_value('Invictus Settings','advance_account'),
                'exchange_rate':0
            })
            new_employee_advance.save()
            frappe.db.commit()
            i.advance=new_employee_advance.name
            i.status=new_employee_advance.status
        
        

    
