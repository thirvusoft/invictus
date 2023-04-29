import frappe

def employee_advance(self,event):
    advance_account=frappe.get_value("Company",self.company,'default_employee_advance_account')
    for i in self.travel_request_advance:
        if i.amount and not i.advance:
            
            new_employee_advance = frappe.new_doc("Employee Advance")
            new_employee_advance.update({
                "employee":self.employee,
                "travel_request":self.name,
                "purpose":self.purpose_of_travel,
                "advance_amount":i.amount,
                "advance_account":advance_account,
                'exchange_rate':0
            })
            new_employee_advance.save()
            frappe.db.commit()
            i.advance=new_employee_advance.name
            i.status=new_employee_advance.status
    self.run_method = lambda arg, **kwargs: 0
    self.save('update')
        
        
def status_change(self,event):
    doc=frappe.get_doc("Travel Request",self.travel_request)
    for i in doc.travel_request_advance:
        if i.advance==self.name:
            frappe.db.set_value('Travel Request Advance',i.name,'status',self.status)

