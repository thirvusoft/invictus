frappe.ui.form.on("Expense Claim", {
	onload: function(frm) {
			if (frm.doc.docstatus == 0) {
				frm.add_custom_button(__('Travel Request'), function () {
					if (!frm.doc.employee) {
						frappe.throw({
							title: __("Mandatory"),
							message: __("Please Select a Employee")
						});
					}
					erpnext.utils.map_current_doc({
						method: "invictus.utils.py.expnese_claim.make_trn",
						source_doctype: "Travel Request",
						target: frm,
						setters: {
							employee: frm.doc.employee,
						},
						get_query_filters: {
							docstatus: 1,
						}
					})
				}, __("Get TRN"));
			}
		}}

)