import frappe

def costing_details(self,event):
    budget=frappe.get_all("CD Budget Allocation",filters={'from_date':['<=',self.creation],'to_date':['>=',self.creation]},pluck='name')

    if budget:
        budget=frappe.get_doc('CD Budget Allocation',budget[0])
        expense=[]

        for row in budget.get(f'{frappe.scrub(self.mode_of_transport)}_budget', []):
            if row.employee_grade == self.employee_grade and row.territory == self.territory:
                expense.append({"funded_amount":row.allocated_amount,'expense_type':row.expense_type})

        self.update({
            'costings':expense
        })


def send_emails(self,events):
    if self.employee_code_approver:
        if self.workflow_state=='Draft':
            subject = ("Travel Request")
            message = (f"Employee ID: {self.employee}<br> Travel Request: <a href='/app/travel-request/{self.name}'>{self.name}</a><br> Territory : {self.territory}")
            recipients=frappe.get_doc("Employee",self.employee_code_approver)
            frappe.sendmail(
                recipients=[recipients.user_id], subject=subject, message=message
            )
        if self.workflow_state=='Objected':
            subject = ("Travel Request Objected")
            message = (f"Travel Request: <a href='/app/travel-request/{self.name}'>{self.name}</a><br> Travel Requested was Objected by {self.employee_code_approver}")
            recipients=frappe.get_doc("Employee",self.employee)
            frappe.sendmail(
                recipients=[recipients.user_id], subject=subject, message=message
            )
        if self.workflow_state=='Approved':
            subject = ("Travel Request Approved")
            message = (f"Travel Request: <a href='/app/travel-request/{self.name}'>{self.name}</a><br> Travel Requested was Approved by {self.employee_code_approver}")
            recipients=frappe.get_doc("Employee",self.employee)
            frappe.sendmail(
                recipients=[recipients.user_id], subject=subject, message=message
            )
        if self.workflow_state=='Rejected':
            subject = ("Travel Request Rejected")
            message = (f"Travel Request: <a href='/app/travel-request/{self.name}'>{self.name}</a><br> Travel Requested was Rejected by {self.employee_code_approver}")
            recipients=frappe.get_doc("Employee",self.employee)
            frappe.sendmail(
                recipients=[recipients.user_id], subject=subject, message=message
            )
        
        