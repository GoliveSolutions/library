// Copyright (c) 2022, Golive-SOlutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Library Member', {
    refresh:frm => {
        frm.add_custom_button(__('create Transaction'), function () {
            make_library_transaction(frm);
        });

	},
});

const make_library_transaction = (frm) => {
    frappe.model.open_mapped_doc({
        method: "library.api.make_library_transaction",
        frm: frm
    });
};