# Copyright (c) 2025, MK and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


import frappe
from frappe.model.document import Document

class Tickets(Document):
    def validate(self):
        
        if self.progress == 100:
            self.status = 'Resolved'
            self.create_notification("resolved")

        elif self.progress < 100:
            self.status = 'Pending'

        
        if self.sla_breach == 1:
            self.create_notification("sla_breach")

    def create_notification(self, notification_type):
        """Create system notifications for ticket events."""
        if self.owner:
            if notification_type == "resolved":
                subject = f'Ticket {self.name} Resolved'
                content = f'Ticket {self.name} has been marked as Resolved.'
            elif notification_type == "sla_breach":
                subject = f'Ticket {self.name} SLA Breached!'
                content = f'Ticket {self.name} has breached the SLA. Immediate action required.'

            frappe.get_doc({
                'doctype': 'Notification Log',
                'subject': subject,
                'content': content,
                'for_user': self.owner, 
                'document_type': 'Tickets',
                'document_name': self.name,
                'type': 'Alert'
            }).insert(ignore_permissions=True)

            frappe.db.commit()  



def create_notification(ticket_id, user):
    
    frappe.get_doc({
        "doctype": "Notification Log",
        "subject": "Your ticket is resolved",
        "email_content": f"The ticket {ticket_id} has been marked as resolved.",
        "for_user": user,
        "type": "Alert"
    }).insert(ignore_permissions=True)


