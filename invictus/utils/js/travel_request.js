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
    sponsored_amount:function(frm){
        frm.set_value('total_amount',frm.sponsored_amount+frm.funded_amount)
    },
    funded_amount:function(frm){
        frm.set_value('total_amount',frm.sponsored_amount+frm.funded_amount)

    }

});

frappe.ui.form.on("Travel Request Costing", {
    sponsored_amount:function(frm,cdt,cdn){  
        console.log(frm.doc.sponsored_amount+frm.doc.funded_amount)      
        frappe.model.set_value(cdt,cdn,'total_amount',frm.doc.sponsored_amount+frm.doc.funded_amount)
    },
    funded_amount:function(frm,cdt,cdn){
        frappe.model.set_value(cdt,cdn,'total_amount',frm.doc.sponsored_amount+frm.doc.funded_amount)

    }

});