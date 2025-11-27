import time
import logging
import threading
from datetime import datetime
import deadline_monitor
import data_persistence
import messaging

class NotificationWorker:
    """Background worker that monitors audit table and sends notifications."""
    
    def __init__(self, check_interval=30):
        self.check_interval = check_interval
        self.running = False
        self.thread = None
    
    def start(self):
        """Starts the background worker thread."""
        if self.running:
            logging.warning("Notification worker already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logging.info("Notification worker started")
    
    def stop(self):
        """Stops the background worker thread."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logging.info("Notification worker stopped")
    
    def _run(self):
        """Main worker loop."""
        while self.running:
            try:
                self.process_notifications()
            except Exception as e:
                logging.error(f"Error in notification worker: {e}")
            
            time.sleep(self.check_interval)
    
    def process_notifications(self):
        """Processes pending notifications from audit table."""
        pending = deadline_monitor.get_pending_notifications()
        
        if not pending:
            return
        
        logging.info(f"Processing {len(pending)} pending notifications")
        
        for event in pending:
            try:
                self.send_project_alert(event)
                deadline_monitor.mark_as_notified(event['audit_id'])
            except Exception as e:
                logging.error(f"Error sending notification for audit {event['audit_id']}: {e}")
    
    def send_project_alert(self, event):
        """Sends alert to all subscribers of a project."""
        project_id = event['project_id']
        
        # Get all subscriptions for this project
        conn = data_persistence.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.user_id, s.notification_channel, u.phone_number, u.name
            FROM subscriptions s
            JOIN users u ON s.user_id = u.user_id
            WHERE s.project_id = ? AND s.notification_enabled = 1
        ''', (project_id,))
        
        subscribers = cursor.fetchall()
        conn.close()
        
        if not subscribers:
            logging.info(f"No subscribers for project {project_id}")
            return
        
        # Format message
        message = self._format_alert_message(event)
        
        # WhatsApp template configuration
        import os
        whatsapp_content_sid = os.getenv('TWILIO_WHATSAPP_CONTENT_SID', 'HXb5b62575e6e4ff6129ad7c8efe1f983e')
        
        # Send to each subscriber
        for sub in subscribers:
            sub_dict = dict(sub)
            phone = sub_dict['phone_number']
            channel = sub_dict['notification_channel']
            
            try:
                if channel == 'wpp':
                    # Prepare template variables for WhatsApp
                    content_vars = self._prepare_whatsapp_variables(event)
                    success, msg_sid, error = messaging.send_whatsapp_message(
                        message, phone, 
                        content_sid=whatsapp_content_sid,
                        content_variables=content_vars
                    )
                else:  # sms
                    success, msg_sid, error = messaging.send_single_sms(message, phone)
                
                if success:
                    logging.info(f"Sent {channel} alert to {phone} for project {project_id}")
                else:
                    logging.error(f"Failed to send {channel} to {phone}: {error}")
            except Exception as e:
                logging.error(f"Error sending to {phone}: {e}")
    
    def _prepare_whatsapp_variables(self, event):
        """Prepares template variables for WhatsApp message."""
        # Adapt based on your template structure
        # Example template expects: {"1": "date", "2": "time"}
        project_name = event['project_name']
        new_date = event.get('new_date', 'N/A')
        
        return {
            "1": new_date.split('T')[0] if 'T' in new_date else new_date,  # Date
            "2": project_name  # Project name
        }
    
    def _format_alert_message(self, event):
        """Formats the alert message based on event type."""
        project_name = event['project_name']
        event_type = event['event_type']
        
        if event_type == 'deadline_expired':
            return f"ALERTA ADAPTT: O prazo do projeto '{project_name}' expirou em {event['new_date']}. Verifique o status."
        elif event_type == 'deadline_extended':
            return f"ATUALIZAÇÃO ADAPTT: O prazo do projeto '{project_name}' foi estendido de {event['old_date']} para {event['new_date']}."
        else:
            return f"ALERTA ADAPTT: Mudança de prazo no projeto '{project_name}'. Novo prazo: {event['new_date']}."

# Global worker instance
notification_worker = NotificationWorker()
