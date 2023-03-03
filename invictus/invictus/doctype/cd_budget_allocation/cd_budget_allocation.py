# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class CDBudgetAllocation(Document):
	def autoname(self):
		if(self.from_date and self.to_date):
			self.name = f"{'/'.join(str(self.from_date).split('-')[::-1])}-{'/'.join(str(self.to_date).split('-')[::-1])}"
		else:
			frappe.throw(msg = _(f'{"From Date" if not self.from_date else "To Date"} is Missing.'), title = _('Value Missing'))
