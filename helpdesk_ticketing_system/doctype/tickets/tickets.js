// Copyright (c) 2025, MK and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Tickets", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Tickets', {
    priority: function(frm) {
        const priority_to_category_map = {
            'High': ['Technical', 'Billing'],  
            'Medium': ['Billing', 'General'], 
            'Low': ['General']                
        };

        const selected_priority = frm.doc.priority;

        if (selected_priority && priority_to_category_map[selected_priority]) {
            frm.set_df_property('category', 'options', priority_to_category_map[selected_priority]);
            frm.set_value('category', priority_to_category_map[selected_priority][0]);
        } else {
            frm.set_df_property('category', 'options', []);
            frm.set_value('category', '');
        }

        frm.refresh_field('category');
    }
});


frappe.ui.form.on('Tickets', {
    refresh: function(frm) {
        if (frm.is_new()) {
            frm.fields_dict['customer'].get_query = function() {
                return {
                    filters: {
                    }
                };
            };
        }
    },

    customer: function(frm) {
        if (frm.doc.customer) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Customer Details",
                    name: frm.doc.customer
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('customer_id', r.message.customer_id);
                        frm.set_value('customer_name', r.message.customer_name);
                        frm.set_value('customer_type', r.message.customer_type);
                        frm.set_value('email_address', r.message.email_address);
                        frm.set_value('address', r.message.address);
                    }
                }
            });
        }
    },

    on_submit: function(frm) {
        if (frm.doc.customer) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Customer",
                    name: frm.doc.customer
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('customer_id', r.message.customer_id);
                        frm.set_value('customer_name', r.message.customer_name);
                        frm.set_value('customer_type', r.message.customer_type);
                        frm.set_value('email_address', r.message.email_address);
                        frm.set_value('address', r.message.address);
                    }
                }
            });
        }
    }
});
