import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_library_transaction(source_name, target_doc=None):
	doclist = get_mapped_doc("Library Member", source_name, {
		"Library Member": {
			"doctype": "Library Transaction",
			"field_map": {
				"library_member": "name",
		},
		}
	}, target_doc)

	return doclist