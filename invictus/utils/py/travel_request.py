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