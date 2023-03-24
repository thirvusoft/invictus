import frappe
from frappe.model.workflow import get_workflow, is_transition_condition_satisfied, has_approval_access
from frappe import _
from frappe.utils import cint
import json

class WorkflowStateError(frappe.ValidationError):
	pass


class WorkflowTransitionError(frappe.ValidationError):
	pass


class WorkflowPermissionError(frappe.ValidationError):
	pass

@frappe.whitelist ()
def get_transitions(
	doc, workflow = None, raise_exception = False):
	"""Return list of possible transitions for the given doc"""
	from frappe.model.document import Document
	if not isinstance(doc, Document):
		doc = frappe.get_doc(frappe.parse_json(doc))
		doc.load_from_db()

	if doc.is_new():
		return []

	doc.check_permission("read")

	workflow = workflow or get_workflow(doc.doctype)
	current_state = doc.get(workflow.workflow_state_field)

	if not current_state:
		if raise_exception:
			raise WorkflowStateError
		else:
			frappe.throw(_("Workflow State not set"), WorkflowStateError)

	transitions = []
	roles = frappe.get_roles()

	approver = None
	employee = frappe.db.get_value('Employee', {'user_id':doc.owner}, 'name')
	if(employee):
		reports_to = frappe.db.get_value('Employee', employee, 'reports_to')
		if(reports_to):
			approver = frappe.db.get_value('Employee', reports_to, 'user_id')
	for transition in workflow.transitions:
		if transition.state == current_state and approver and approver == frappe.session.user:
			if not is_transition_condition_satisfied(transition, doc):
				continue
			transition.user_allowed = approver
			transitions.append(transition.as_dict())

	return transitions

@frappe.whitelist()
def apply_workflow(doc, action):
	"""Allow workflow action on the current doc"""
	doc = frappe.get_doc(frappe.parse_json(doc))
	workflow = get_workflow(doc.doctype)
	transitions = get_transitions(doc, workflow)
	user = frappe.session.user

	# find the transition
	transition = None
	for t in transitions:
		if t.action == action:
			transition = t

	if not transition:
		frappe.throw(_("Not a valid Workflow Action"), WorkflowTransitionError)

	if not has_approval_access(user, doc, transition):
		frappe.throw(_("Self approval is not allowed"))

	# update workflow state field
	doc.set(workflow.workflow_state_field, transition.next_state)

	# find settings for the next state
	next_state = [d for d in workflow.states if d.state == transition.next_state][0]

	# update any additional field
	if next_state.update_field:
		doc.set(next_state.update_field, next_state.update_value)

	new_docstatus = cint(next_state.doc_status)
	if doc.docstatus == 0 and new_docstatus == 0:
		doc.save()
	elif doc.docstatus == 0 and new_docstatus == 1:
		doc.submit()
	elif doc.docstatus == 1 and new_docstatus == 1:
		doc.save()
	elif doc.docstatus == 1 and new_docstatus == 2:
		doc.cancel()
	else:
		frappe.throw(_("Illegal Document Status for {0}").format(next_state.state))

	doc.add_comment("Workflow", _(next_state.state))
	return doc

@frappe.whitelist()
def get_doc_state_approver(state, doc):
	if isinstance(state, str):
		state = json.loads(state)
	if isinstance(doc, str):
		doc = json.loads(doc)
	approver = None
	employee = frappe.db.get_value('Employee', {'user_id':doc.get('owner')}, 'name')
	if(employee):
		reports_to = frappe.db.get_value('Employee', employee, 'reports_to')
		if(reports_to):
			approver = frappe.db.get_value('Employee', reports_to, 'user_id')
	state['allow_edit'] = approver
	state['user_allowed'] = approver