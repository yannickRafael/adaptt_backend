import json
import sqlite3
from datetime import datetime
from db_manager import get_db_connection

def insert_or_update_project(project_id, data):
    """Inserts or updates a project in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Use 'title' as per OC4IDS standard, fallback to 'name' for compatibility
    project_name = data.get('title') or data.get('name', 'Unknown')
    status = data.get('status', 'Unknown')
    data_raw = json.dumps(data)
    last_sync = datetime.now()

    # Check if project exists
    cursor.execute('SELECT project_id FROM projects WHERE project_id = ?', (project_id,))
    exists = cursor.fetchone()
    
    if exists:
        # Update existing project, preserving transparency scores
        cursor.execute('''
            UPDATE projects 
            SET project_name = ?, status = ?, data_raw = ?, last_sync = ?
            WHERE project_id = ?
        ''', (project_name, status, data_raw, last_sync, project_id))
    else:
        # Insert new project
        cursor.execute('''
            INSERT INTO projects (project_id, project_name, status, data_raw, last_sync)
            VALUES (?, ?, ?, ?, ?)
        ''', (project_id, project_name, status, data_raw, last_sync))
    
    conn.commit()
    conn.close()

def insert_document_status(project_id, documents):
    """Updates the document status for a project."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing documents for this project
    cursor.execute('DELETE FROM project_documents WHERE project_id = ?', (project_id,))

    for doc in documents:
        doc_type = doc.get('type')
        is_published = 1 if doc.get('url') else 0 # Assuming 'url' presence means published
        critical_weight = doc.get('weight', 0.0) # Placeholder logic

        cursor.execute('''
            INSERT INTO project_documents (project_id, doc_type, is_published, critical_weight)
            VALUES (?, ?, ?, ?)
        ''', (project_id, doc_type, is_published, critical_weight))

    conn.commit()
    conn.close()

def get_raw_project_data(project_id):
    """Retrieves the raw JSON data for a project."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT data_raw, transparency_score, alert_color FROM projects WHERE project_id = ?', (project_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        data = json.loads(row['data_raw'])
        data['transparency_score'] = row['transparency_score']
        data['alert_color'] = row['alert_color']
        return data
    return None

def get_all_projects():
    """Retrieves all projects from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT project_id, project_name, status, last_sync, transparency_score, alert_color FROM projects')
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_project_documents(project_id):
    """Retrieves documents for a specific project."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM project_documents WHERE project_id = ?', (project_id,))
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def insert_or_update_location(location):
    """Inserts or updates a location in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO locations (id, name, region, country)
        VALUES (?, ?, ?, ?)
    ''', (location['id'], location['name'], location['region'], location['country']))
    
    conn.commit()
    conn.close()

def get_all_locations():
    """Retrieves all locations from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM locations')
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

import re

def validate_phone_number(phone):
    """
    Validates Mozambican phone number format.
    Accepts: +258 XX XXX XXXX, +258XXXXXXXXX, 8XXXXXXXX, 9XXXXXXXX
    """
    # Pattern for Mozambican mobile numbers
    # +258 followed by 8X or 9X and 7 more digits
    # OR just 8X/9X followed by 7 digits
    pattern = r'^(\+258\s?)?[89]\d{8}$'
    
    # Remove spaces for validation
    phone_clean = phone.replace(' ', '')
    
    return re.match(pattern, phone_clean) is not None

def region_exists(region_id):
    """Checks if a region exists in the locations table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM locations WHERE id = ?', (region_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result is not None

def register_user(name, phone_number, region_id):
    """
    Registers a new user with validation.
    Returns: (success: bool, message: str, user_id: int or None)
    """
    # Validate phone number
    if not validate_phone_number(phone_number):
        return False, "Número de telefone inválido. Use o formato moçambicano (+258 XX XXX XXXX ou 8X/9X XXXXXXX).", None
    
    # Validate region
    if not region_exists(region_id):
        return False, "Região não existe na base de dados.", None
    
    # Normalize phone number (remove spaces, ensure +258 prefix)
    phone_clean = phone_number.replace(' ', '')
    if not phone_clean.startswith('+258'):
        phone_clean = '+258' + phone_clean
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (name, phone_number, region_id)
            VALUES (?, ?, ?)
        ''', (name, phone_clean, region_id))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return True, "Utilizador registado com sucesso.", user_id
    except sqlite3.IntegrityError:
        return False, "Este número de telefone já está registado.", None
    except Exception as e:
        return False, f"Erro ao registar utilizador: {str(e)}", None

def get_user_by_phone(phone_number):
    """Retrieves a user by phone number."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE phone_number = ?', (phone_number,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None

def subscribe_to_project(user_id, project_id, notification_channel='sms'):
    """
    Subscribes a user to a project.
    Returns: (success: bool, message: str, subscription_id: int or None)
    """
    # Validate notification channel
    if notification_channel not in ['sms', 'wpp']:
        return False, "Canal de notificação inválido. Use 'sms' ou 'wpp'.", None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO subscriptions (user_id, project_id, notification_channel)
            VALUES (?, ?, ?)
        ''', (user_id, project_id, notification_channel))
        
        subscription_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return True, "Subscrição realizada com sucesso.", subscription_id
    except sqlite3.IntegrityError:
        return False, "Já está subscrito a este projeto.", None
    except Exception as e:
        return False, f"Erro ao subscrever: {str(e)}", None

def unsubscribe_from_project(user_id, project_id):
    """
    Unsubscribes a user from a project.
    Returns: (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM subscriptions
            WHERE user_id = ? AND project_id = ?
        ''', (user_id, project_id))
        
        rows_deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        if rows_deleted > 0:
            return True, "Subscrição cancelada com sucesso."
        else:
            return False, "Subscrição não encontrada."
    except Exception as e:
        return False, f"Erro ao cancelar subscrição: {str(e)}"

def get_user_subscriptions(user_id):
    """Retrieves all subscriptions for a user with project details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.subscription_id, s.user_id, s.project_id, s.subscribed_at, s.notification_enabled,
               s.notification_channel, p.project_name, p.status, p.transparency_score, p.alert_color
        FROM subscriptions s
        JOIN projects p ON s.project_id = p.project_id
        WHERE s.user_id = ?
    ''', (user_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def is_subscribed(user_id, project_id):
    """Checks if a user is subscribed to a project."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT subscription_id FROM subscriptions
        WHERE user_id = ? AND project_id = ?
    ''', (user_id, project_id))
    
    result = cursor.fetchone()
    conn.close()
    
    return result is not None
