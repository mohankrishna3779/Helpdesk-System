import frappe
from frappe.utils import get_datetime
from frappe.core.doctype.communication.email import make

def send_ticket_report():

    query = """
    SELECT
        ticket_id AS "Ticket ID",
        subject AS "Subject",
        description AS "Description",
        customer AS "Customer",
        priority AS "Priority",
        category AS "Category",
        progress AS "Progress",
        status AS "Status",
        creation_date AS "Created On",
        resolved_date AS "Resolved On",
        sla AS "SLA Deadline",
        assigned_to AS "Assigned To",
        times AS "Response Time",
        over_due AS "Over Due",
        AVG(TIME_TO_SEC(`times`)) / 3600 AS "Avg Response Time (Hours)"
    FROM
        `tabTickets`
    WHERE
        status = 'Pending'  -- Filter for Pending tickets
        AND over_due > 0   -- Filter for tickets where over_due > 0
    ORDER BY
        sla ASC;
    """
    
    result = frappe.db.sql(query, as_dict=True)

    
    message = "Pending Ticket Report (12 Hour Update):\n\n"
    for row in result:
        message += f"Ticket ID: {row['Ticket ID']}, Subject: {row['Subject']}, Status: {row['Status']}, SLA Deadline: {row['SLA Deadline']}\n"
    
    
    make(
        recipients="admin@example.com",  
        subject="Pending Tickets Status Update",
        content=message
    )


send_ticket_report()
