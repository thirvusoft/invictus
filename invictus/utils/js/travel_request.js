frappe.ui.form.on("Travel Request", {
    onload: function (frm) {
        frm.set_query('mode_of_transport', function () {
            return {
                filters: {
                    'is_group': 1
                }
            }
        });
    },

});

frappe.ui.form.on("Travel Request Costing", {
    sponsored_amount:function(frm,cdt,cdn){ 
        let row = locals[cdt][cdn] 

        frappe.model.set_value(cdt,cdn,'total_amount',row.sponsored_amount+row.funded_amount)
    },
    funded_amount:function(frm,cdt,cdn){
        let row = locals[cdt][cdn] 
        frappe.model.set_value(cdt,cdn,'total_amount',row.sponsored_amount+row.funded_amount)

    }

});