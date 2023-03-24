frappe.ui.form.on('Travel Request', {
    refresh: function(frm){
        if(frm.wrapper.querySelector('span[data-label=Reject]')){
            frm.rejected = false;
            frm.wrapper.querySelector('span[data-label=Reject]').parentElement.onclick=function(){
                frm.rejected  = true;
            } 
        }
        if(frm.wrapper.querySelector('span[data-label=Object]')){
            frm.objected = false;
            frm.wrapper.querySelector('span[data-label=Object]').parentElement.onclick=function(){
                frm.objected  = true;
            } 
        }
        if(frm.wrapper.querySelector('span[data-label=Re-Request]')){
            frm.rerequest = false;
            frm.wrapper.querySelector('span[data-label=Re-Request]').parentElement.onclick=function(){
                frm.rerequest  = true;
            } 
        }
    },
    before_workflow_action(frm){
		if(frm.rejected == true){
			frappe.validated = false;
            var dialog = new frappe.ui.Dialog({
                title:'Reject Reason',
                fields:[{'fieldname':'lost_reason', 'label':'Reject Reason', 'fieldtype':'Small Text', 'reqd':1}],
                primary_action(data){
                    frm.set_value('rejected_reason', data['lost_reason'])
                    reject(frm)
                    dialog.hide()
                }
            })	
            dialog.show()
		}
        else if(frm.objected == true){
			frappe.validated = false;
            var dialog = new frappe.ui.Dialog({
                title:'Object Reason',
                fields:[{'fieldname':'object_reason', 'label':'Objecting Reason', 'fieldtype':'Small Text', 'reqd':1}],
                primary_action(data){
                    object(frm, data)
                    dialog.hide()
                }
            })	
            dialog.show()
		}
        else if(frm.rerequest == true){
			frappe.validated = false;
            var dialog = new frappe.ui.Dialog({
                title:'Re-Request Reason',
                fields:[{'fieldname':'rerequest_reason', 'label':'Re-Requesting Reason', 'fieldtype':'Small Text', 'reqd':1}],
                primary_action(data){
                    frm.set_value('reiteration_count',frm.doc.reiteration_count+1)
                    rerequest(frm, data)
                    dialog.hide()
                }
            })	
            dialog.show()
		}
	},
    async create_advance_entry(frm){
        let meta = await frappe.xcall("invictus.invictus.utils.py.travel_request.get_meta", {doc:'Employee Advance'}) 
		let fields = meta.fields;

		// prepare a list of mandatory, bold and allow in quick entry fields
		let mandatory = fields.filter(df => {
			return ((df.allow_in_quick_entry) && !df.read_only);
		});
      mandatory.forEach((df)=>{
        if(df.options == 'Account'){
            df['filters'] = {'is_group':0}
        }
      })
        var dialog = new frappe.ui.Dialog({
            title :'New Employee Advance',
            fields:mandatory,
            primary_action_label: __('Save'),
            primary_action: function(data){
                data['travel_request'] = frm.docname
                data['exchange_rate'] = 1
				data['employee'] = frm.doc.employee
                data['purpose'] = frm.doc.purpose_of_travel
				data['company'] = frm.doc.company
                frappe.xcall("invictus.invictus.utils.py.travel_request.create_employee_advance", {data:data, async:false}).then((r)=>{
                    dialog.set_primary_action('Submit', frappe.confirm(`Permanently Submit Employee Advance ${r.name}`,
                        function() {
                            frm.reload_doc()
                            frappe.xcall("invictus.invictus.utils.py.travel_request.submit_employee_advance", {emp_adv:r.name})
                            dialog.hide();
					    },
                        function(){
                            frm.reload_doc()
                            dialog.hide();
                        }, 
                    ))
					
				})
            }
        })
        dialog.show()
    }
})

function reject(frm){
    frappe.xcall('frappe.model.workflow.apply_workflow',
            {doc: frm.doc, action: 'Reject'})
            .then((doc) => {
                frappe.model.sync(doc);
                frm.refresh();
                frm.rejected = false;
                frm.selected_workflow_action = null;
                frm.script_manager.trigger("after_workflow_action");
            });
}
function object(frm, data){
    frappe.xcall('invictus.invictus.utils.py.travel_request.add_comment', 
            {doc:frm.docname, comment:data['object_reason'], action: 'Object'})
            .then(()=>{
                frappe.xcall('frappe.model.workflow.apply_workflow',
                {doc: frm.doc, action: 'Object'})
                .then((doc) => {
                    frappe.model.sync(doc);
                    frm.reload_doc();
                    frm.objected = false;
                    frm.selected_workflow_action = null;
                    frm.script_manager.trigger("after_workflow_action");
                });
            })
    
}

function rerequest(frm, data){
    frappe.xcall('invictus.invictus.utils.py.travel_request.add_comment', 
            {doc:frm.docname, comment:data['rerequest_reason'], action: 'Re-Request'})
            .then(()=>{
                frappe.xcall('frappe.model.workflow.apply_workflow',
                {doc: frm.doc, action: 'Re-Request'})
                .then((doc) => {
                    frappe.model.sync(doc);
                    frm.reload_doc();
                    frm.rerequest = false;
                    frm.selected_workflow_action = null;
                    frm.script_manager.trigger("after_workflow_action");
                });
            })
    
}