// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mode of Transport', {
	refresh: function(frm) {
		frm.set_query('parent_mode_of_transport', ()=>{
			return {
				filters : {
					'is_group':1
				}
			}
		})
	}
});
