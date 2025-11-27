import json
import logging
from datetime import datetime
from db_manager import get_db_connection

def detect_deadline_changes(project_id, new_data, old_data):
    """
    Detects deadline changes between old and new project data.
    Returns list of audit events to log.
    """
    events = []
    
    # Extract implementation period end dates
    new_impl_end = None
    old_impl_end = None
    
    if isinstance(new_data, dict):
        impl_period = new_data.get('implementationPeriod', {})
        if isinstance(impl_period, dict):
            new_impl_end = impl_period.get('endDate')
    
    if isinstance(old_data, dict):
        impl_period = old_data.get('implementationPeriod', {})
        if isinstance(impl_period, dict):
            old_impl_end = impl_period.get('endDate')
    
    # Check if deadline changed
    if old_impl_end and new_impl_end and old_impl_end != new_impl_end:
        try:
            old_date = datetime.fromisoformat(old_impl_end.replace('Z', '+00:00'))
            new_date = datetime.fromisoformat(new_impl_end.replace('Z', '+00:00'))
            
            if new_date > old_date:
                event_type = 'deadline_extended'
            else:
                event_type = 'deadline_changed'
            
            events.append({
                'project_id': project_id,
                'event_type': event_type,
                'old_date': old_impl_end,
                'new_date': new_impl_end
            })
        except Exception as e:
            logging.error(f"Error parsing dates for project {project_id}: {e}")
    
    # Check if deadline expired
    if new_impl_end:
        try:
            end_date = datetime.fromisoformat(new_impl_end.replace('Z', '+00:00'))
            now = datetime.now(end_date.tzinfo)
            
            if end_date < now:
                # Check if we already logged this expiration
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT audit_id FROM project_audit 
                    WHERE project_id = ? AND event_type = 'deadline_expired' AND new_date = ?
                ''', (project_id, new_impl_end))
                
                if not cursor.fetchone():
                    events.append({
                        'project_id': project_id,
                        'event_type': 'deadline_expired',
                        'old_date': None,
                        'new_date': new_impl_end
                    })
                conn.close()
        except Exception as e:
            logging.error(f"Error checking expiration for project {project_id}: {e}")
    
    return events

def log_audit_event(event):
    """Logs an audit event to the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO project_audit (project_id, event_type, old_date, new_date)
            VALUES (?, ?, ?, ?)
        ''', (event['project_id'], event['event_type'], event.get('old_date'), event['new_date']))
        
        audit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logging.info(f"Logged audit event {audit_id}: {event['event_type']} for project {event['project_id']}")
        return audit_id
    except Exception as e:
        logging.error(f"Error logging audit event: {e}")
        return None

def get_pending_notifications():
    """Retrieves audit events that haven't been notified yet."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.audit_id, a.project_id, a.event_type, a.old_date, a.new_date, a.detected_at,
               p.project_name
        FROM project_audit a
        JOIN projects p ON a.project_id = p.project_id
        WHERE a.notified = 0
        ORDER BY a.detected_at ASC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def mark_as_notified(audit_id):
    """Marks an audit event as notified."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE project_audit SET notified = 1 WHERE audit_id = ?', (audit_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logging.error(f"Error marking audit {audit_id} as notified: {e}")
        return False
