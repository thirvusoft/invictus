import frappe

def costing_details(self,event):
    budget=frappe.get_all("CD Budget Allocation",filters={'from_date':['<=',self.creation],'to_date':['>=',self.creation]},pluck='name')

    if budget:
        budget=frappe.get_doc('CD Budget Allocation',budget[0])
        expense=[]

        for row in budget.get(f'{frappe.scrub(self.mode_of_transport)}_budget', []):
            if row.employee_grade == self.employee_grade and row.territory == self.territory:
                expense.append({"funded_amount":row.allocated_amount,'expense_type':row.expense_type,'total_amount':row.allocated_amount})

        self.update({
            'costings':expense
        })


def send_emails(self,events):
    if self.employee_code_approver:
        if self.docstatus=='0':
            subject = ("Travel Request")
            message = (f"Employee ID: {self.employee}<br> Travel Request: <a href='/app/travel-request/{self.name}'>{self.name}</a><br> Territory : {self.territory}")
            recipients=frappe.get_doc("Employee",self.employee_code_approver)
            frappe.sendmail(
                recipients=[recipients.user_id], subject=subject, message=message
            )
        if self.travel_request_status=='Objected':
            subject = ("Travel Request Objected")
            message = (f"Travel Request: <a href='/app/travel-request/{self.name}'>{self.name}</a><br> Travel Requested was Objected by {self.employee_code_approver}")
            recipients=frappe.get_doc("Employee",self.employee)
            frappe.sendmail(
                recipients=[recipients.user_id], subject=subject, message=message
            )
        if self.travel_request_status=='Approved':
            subject = ("Travel Request Approved")
            message = (f"Travel Request: <a href='/app/travel-request/{self.name}'>{self.name}</a><br> Travel Requested was Approved by {self.employee_code_approver}")
            recipients=frappe.get_doc("Employee",self.employee)
            frappe.sendmail(
                recipients=[recipients.user_id], subject=subject, message=message
            )
        if self.travel_request_status=='Rejected':
            subject = ("Travel Request Rejected")
            message = (f"Travel Request: <a href='/app/travel-request/{self.name}'>{self.name}</a><br> Travel Requested was Rejected by {self.employee_code_approver}")
            recipients=frappe.get_doc("Employee",self.employee)
            frappe.sendmail(
                recipients=[recipients.user_id], subject=subject, message=message
            )
        
        
def travel_approve(self,event):
    reports_to=frappe.get_value("Employee",self.employee, "reports_to")
    employee_approver=""
    if reports_to:
        employee_approver = frappe.get_value("Employee",reports_to, "user_id")
    session_user=frappe.session.user
    if employee_approver!=session_user :
        frappe.throw("You have no permission to submit this document.")
    

def status_update(self,evevnt):
    for i in self.travel_request_advance:
        status=frappe.get_value('Employee Advance',i.advance,'status')
        frappe.db.set_value('Travel Request Advance',i.name,'status',status)
    self.reload()

        
def totals(self,event):
    total_req=0
    total_recieved=0

    if self.travel_request_advance:
        for i in self.travel_request_advance:
            total_req=total_req+i.amount
            if i.status=="Paid":
                total_recieved=total_recieved+i.amount
    if self.total_eligible_amount:
        self.total_allocated_amount=self.total_eligible_amount

    self.total_advance_requested=total_req
    self.total_advance_received=total_recieved
def eligibal_amount(self,event):
    eligible=0
    if self.costings:
        for j in self.costings:
            eligible=eligible+j.total_amount
    
    self.total_eligible_amount =eligible

    
            

