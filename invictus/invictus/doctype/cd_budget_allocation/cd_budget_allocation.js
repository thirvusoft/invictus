// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('CD Budget Allocation', {
	refresh: function(frm) {
		if(frm.is_new()){
			frm.set_value('company', frappe.defaults.get_user_default('company'))
			frm.refresh_field('company')
		}
		frm.set_query('territory', 'air_budget',function(frm){
            return {
                filters:{
                    'parent_territory':'All Territories'
                }
            }
        })
		frm.set_query('territory', 'road_budget',function(frm){
            return {
                filters:{
                    'parent_territory':'All Territories'
                }
            }
        })
		frm.set_query('territory', 'rail_budget',function(frm){
            return {
                filters:{
                    'parent_territory':'All Territories'
                }
            }
        })
	}
});
