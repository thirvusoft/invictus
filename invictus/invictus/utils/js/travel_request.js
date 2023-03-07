frappe.ui.form.on('Travel Request', {
    refresh: function(frm){
        if(frm.wrapper.querySelector('span[data-label=Reject]')){
            frm.rejected = false;
            frm.wrapper.querySelector('span[data-label=Reject]').onclick=function(){
                frm.rejected  = true;
            } 
        }
        if(frm.wrapper.querySelector('span[data-label=Object]')){
            frm.objected = false;
            frm.wrapper.querySelector('span[data-label=Object]').onclick=function(){
                frm.objected  = true;
            } 
        }
        if(frm.wrapper.querySelector('span[data-label=Re-Request]')){
            frm.rerequest = false;
            frm.wrapper.querySelector('span[data-label=Re-Request]').onclick=function(){
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
                    rerequest(frm, data)
                    dialog.hide()
                }
            })	
            dialog.show()
		}
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