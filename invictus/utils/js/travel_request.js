frappe.ui.form.on("Travel Request", {
    onload: function (frm) {
        frm.set_query('mode_of_transport', function () {
            return {
                filters: {
                    'is_group': 1
                }
            }
        });
    }
});