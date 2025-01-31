# Copyright (c) 2025, MK and contributors
# For license information, please see license.txt

# import frappe

import frappe
from datetime import datetime

def get_average_resolution_time():
    try:
        # Fetch tickets with creation and resolution_date
        tickets = frappe.db.sql("""
            SELECT creation, resolution_date
            FROM `tabTicket`
            WHERE resolution_date IS NOT NULL
        """, as_dict=True)

        # If no tickets found, return 0 and print a message
        if not tickets:
            frappe.msgprint("No tickets with a resolution date found.")
            return 0

        total_time = 0
        valid_tickets = 0

        for t in tickets:
            try:
                # Log ticket data for debugging
                frappe.log_error(f"Processing ticket: {t}", "Ticket Debug")
                
                # Parse creation and resolution_date fields
                creation = datetime.strptime(str(t['creation']), "%Y-%m-%d %H:%M:%S")
                resolution_date = datetime.strptime(str(t['resolution_date']), "%Y-%m-%d %H:%M:%S")
                
                # Calculate total seconds and add to total_time
                total_time += (resolution_date - creation).total_seconds()
                valid_tickets += 1
            except Exception as e:
                # Log error and skip the problematic ticket
                frappe.log_error(f"Error processing ticket {t}: {str(e)}", "Ticket Processing Error")
                continue

        # Calculate average resolution time in hours
        average_time = total_time / valid_tickets / 3600 if valid_tickets else 0

        # Log the final result for verification
        frappe.log_error(f"Average Resolution Time: {average_time} hours", "Calculation Result")
        
        return average_time

    except Exception as e:
        # Log any unexpected errors
        frappe.log_error(f"Unexpected error: {str(e)}", "Unexpected Error")
        frappe.throw("An error occurred while calculating the average resolution time.")
