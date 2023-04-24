frappe.ui.form.on("Travel Request Costing", {
    sponsored_amount:function(frm){
        frm.set_value('total_amount',frm.sponsored_amount+frm.funded_amount)
    },
    funded_amount:function(frm){
        frm.set_value('total_amount',frm.sponsored_amount+frm.funded_amount)

    }

});