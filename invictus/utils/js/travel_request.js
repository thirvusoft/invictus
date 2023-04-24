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