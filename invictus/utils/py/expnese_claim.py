import frappe
from frappe.model.mapper import get_mapped_doc

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
