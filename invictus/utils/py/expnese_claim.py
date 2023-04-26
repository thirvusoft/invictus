import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import nowdate
import datetime
from datetime import datetime as dt

@frappe.whitelist()
def make_trn(source_name, target_doc=None):
    def remove_empty_rows(source, target):
        ecd = []
        for row in target.expenses:
            if row.expense_type:
                ecd.append(row)
        target.update({
            "expenses": ecd
        })
    doc = get_mapped_doc(
        "Travel Request",
        source_name,
        {
            "Travel Request": {
                "doctype": "Expense Claim",
                "validation": {
                    "docstatus": ["=", 1],
                },
            },
            "Travel Request Costing": {
                "doctype": 'Expense Claim Detail',
                "field_map": {
                    "expense_type":"expense_type",
                    "total_amount":"amount",
                    "total_amount":"sanctioned_amount",
                    "creation":"expense_date",
                    "docname":"travel_request_id"
                    
                },

            },
        },
        target_doc,
        remove_empty_rows
    )

    return doc

def expense_cycle(self,event):
    if self.expenses:
        for i in self.expenses:
            trn_creation=frappe.get_doc("Travel Request",i.travel_request_id)
            
            trn_month=int(datetime.datetime.strftime(trn_creation.creation,'%m'))
            trn_date=int(datetime.datetime.strftime(trn_creation.creation,'%d'))
            trn_year=int(datetime.datetime.strftime(trn_creation.creation,'%Y'))
            creation=datetime.datetime.strptime(self.creation,'%Y-%m-%d %H:%M:%S.%f')

            exp_month=int(datetime.datetime.strftime(creation,'%m'))
            exp_date=int(datetime.datetime.strftime(creation,'%d'))
            if trn_date in range(1,16):
                if exp_date > 21:
                    frappe.throw("Expense Claim Date is Overdued")
            if trn_date >15:
                todate= dt(year=trn_year,month=trn_month+1,day=6,hour=0,minute=0,second=0)
                if  (creation>todate):
                    frappe.throw("Expense Claim Date is Overdued")
                    
                
            

            


def expense_validation(self,event):
    if self.expenses:
        for i in self.expenses:
            trn=frappe.get_doc("Travel Request",i.travel_request_id)
            old_expense=sum(frappe.get_all("Expense Claim Detail",filters={'travel_request_id':i.travel_request_id,'expense_type':i.expense_type,'docstatus':1},fields=['sum(amount)'], group_by='travel_request_id'))
            if trn.costings:
                allocated_amount=0
                for j in trn.costings:
                    if j.expense_type==i.expense_type:
                        allocated_amount=allocated_amount+j.funded_amount
                if allocated_amount==0:
                    frappe.throw('The Expense Type is Mismatched with Travel Request')
                        
                if allocated_amount!= i.amount+old_expense:
                    frappe.throw('The Amount is Mismatched with Travel Request')  

            
                

                        

            
            
            
    

