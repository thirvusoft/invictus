# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class CDBudgetAllocation(Document):
    def autoname(self):
        if(self.from_date and self.to_date):
            self.name = f"{'-'.join(str(self.from_date).split('-')[::-1])}-{'-'.join(str(self.to_date).split('-')[::-1])}"
        else:
            frappe.throw(msg = _(f'{"From Date" if not self.from_date else "To Date"} is Missing.'), title = _('Value Missing'))

    def validate(self):
        fromdate=frappe.get_all('CD Budget Allocation',filters={'from_date':['<=',self.from_date],'name':['!=',self.name]},pluck='name')
        todate=frappe.get_all('CD Budget Allocation',filters={'to_date':['>=',self.to_date],'name':['!=',self.name],'docstatus':['!=',2]},pluck='name')
        common_dates=[]
        for i in todate:
            if i in fromdate:
                common_dates.append(i)
        if common_dates:
            frappe.throw(f"From Date and To Date is Overlapped with {', '.join(common_dates)}")
