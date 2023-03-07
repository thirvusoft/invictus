frappe.ui.form.States = class States extends frappe.ui.form.States {
    async show_actions() {
		var added = false;
		var me = this;
		// if the loaded doc is dirty, don't show workflow buttons
		if (this.frm.doc.__unsaved===1) {
			return;
		}

		function has_approval_access(transition) {
			let approval_access = false;
			const user = frappe.session.user;
			if (user === 'Administrator'
				|| transition.allow_self_approval
				|| user !== me.frm.doc.owner) {
				approval_access = true;
			}
			return approval_access;
		}
		frappe.workflow.get_transitions(this.frm.doc).then(async transitions => {
			this.frm.page.clear_actions_menu();
			transitions.forEach(d => {
				if (frappe.session.user == d.user_allowed ) {
				// if (frappe.user_roles.includes(d.allowed) && has_approval_access(d)) {
					added = true;
					me.frm.rejected = false;
					me.frm.objected = false;
					me.frm.rerequest = false
					me.frm.page.add_action_item(__(d.action), function() {
						// set the workflow_action for use in form scripts
						me.frm.selected_workflow_action = d.action;
						
						me.frm.script_manager.trigger('before_workflow_action').then(() => {
							if(!me.frm.rejected && !me.frm.objected && !me.frm.rerequest){
							frappe.xcall('frappe.model.workflow.apply_workflow',
								{doc: me.frm.doc, action: d.action})
								.then((doc) => {
									frappe.model.sync(doc);
									me.frm.refresh();
									me.frm.selected_workflow_action = null;
									me.frm.script_manager.trigger("after_workflow_action");
								});
							}
						});
					});
				}
			});

			this.setup_btn(added);
		});

	}
}

frappe.workflow['is_read_only'] = function(doctype, name) {
	var state_fieldname = frappe.workflow.get_state_fieldname(doctype);
	if(state_fieldname) {
		var doc = locals[doctype][name];
		if(!doc)
			return false;
		if(doc.__islocal)
			return false;

		var state = doc[state_fieldname] ||
			frappe.workflow.get_default_state(doctype, doc.docstatus);

		var allow_edit = state ? frappe.workflow.get_document_state(doctype, state) && frappe.workflow.get_document_state(doctype, state).user_allowed : null;
		if(! (frappe.session.user == allow_edit)) {
			return true;
		}
	}
	return false;
}