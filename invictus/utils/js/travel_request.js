frappe.ui.form.on("Travel Request", {
    onload: async function (frm) {
        frm.set_query('mode_of_transport', function () {
            return {
                filters: {
                    'is_group': 1
                }
            }
        });
        cur_frm.email_field = cur_frm.doc.contact_email == frappe.session.user ? "prefered_email":"contact_email"
        let emp= await frappe.db.get_value("Employee",{user_id:frappe.session.user},'name')
        if (cur_frm.is_new()){
            cur_frm.set_value('employee',emp.message.name)
        }
    }



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