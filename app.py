from flask import Flask, jsonify, request
from flasgger import Swagger
import data_persistence
import logging
import os

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """
    Get all projects
    ---
    responses:
      200:
        description: A list of projects
        schema:
          type: array
          items:
            type: object
            properties:
              project_id:
                type: string
              project_name:
                type: string
              status:
                type: string
              last_sync:
                type: string
    """
    projects = data_persistence.get_all_projects()
    return jsonify(projects)

@app.route('/api/projects/<project_id>', methods=['GET'])
def get_project_details(project_id):
    """
    Get project details
    ---
    parameters:
      - name: project_id
        in: path
        type: string
        required: true
        description: The ID of the project
    responses:
      200:
        description: Project details
      404:
        description: Project not found
    """
    project = data_persistence.get_raw_project_data(project_id)
    if project:
        return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404

@app.route('/api/projects/<project_id>/documents', methods=['GET'])
def get_project_documents(project_id):
    """
    Get project documents
    ---
    parameters:
      - name: project_id
        in: path
        type: string
        required: true
        description: The ID of the project
    responses:
      200:
        description: List of project documents
    """
    documents = data_persistence.get_project_documents(project_id)
    return jsonify(documents)

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """
    Get all locations
    ---
    responses:
      200:
        description: A list of locations
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              name:
                type: string
              region:
                type: string
              country:
                type: string
    """
    locations = data_persistence.get_all_locations()
    return jsonify(locations)

@app.route('/api/users/register', methods=['POST'])
def register_user():
    """
    Register a new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - phone_number
            - region_id
          properties:
            name:
              type: string
              description: User's full name
            phone_number:
              type: string
              description: Mozambican phone number (+258 XX XXX XXXX or 8X/9X XXXXXXX)
            region_id:
              type: string
              description: Region ID from locations table
    responses:
      201:
        description: User registered successfully
      400:
        description: Validation error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    name = data.get('name')
    phone_number = data.get('phone_number')
    region_id = data.get('region_id')
    
    if not all([name, phone_number, region_id]):
        return jsonify({'error': 'Nome, número de telefone e região são obrigatórios'}), 400
    
    success, message, user_id = data_persistence.register_user(name, phone_number, region_id)
    
    if success:
        return jsonify({
            'message': message,
            'user_id': user_id,
            'name': name,
            'phone_number': phone_number.replace(' ', '') if not phone_number.startswith('+258') else phone_number,
            'region_id': region_id
        }), 201
    else:
        return jsonify({'error': message}), 400

@app.route('/api/subscriptions', methods=['POST'])
def create_subscription():
    """
    Subscribe to a project
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - project_id
          properties:
            user_id:
              type: integer
              description: User ID
            project_id:
              type: string
              description: Project ID
            notification_channel:
              type: string
              description: Notification channel (sms or wpp)
              enum: [sms, wpp]
              default: sms
    responses:
      201:
        description: Subscription created successfully
      400:
        description: Validation error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    user_id = data.get('user_id')
    project_id = data.get('project_id')
    notification_channel = data.get('notification_channel', 'sms')
    
    if not all([user_id, project_id]):
        return jsonify({'error': 'user_id e project_id são obrigatórios'}), 400
    
    success, message, subscription_id = data_persistence.subscribe_to_project(user_id, project_id, notification_channel)
    
    if success:
        return jsonify({
            'message': message,
            'subscription_id': subscription_id,
            'user_id': user_id,
            'project_id': project_id,
            'notification_channel': notification_channel
        }), 201
    else:
        return jsonify({'error': message}), 400

@app.route('/api/subscriptions', methods=['DELETE'])
def delete_subscription():
    """
    Unsubscribe from a project
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - project_id
          properties:
            user_id:
              type: integer
            project_id:
              type: string
    responses:
      200:
        description: Unsubscribed successfully
      400:
        description: Error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    user_id = data.get('user_id')
    project_id = data.get('project_id')
    
    if not all([user_id, project_id]):
        return jsonify({'error': 'user_id e project_id são obrigatórios'}), 400
    
    success, message = data_persistence.unsubscribe_from_project(user_id, project_id)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@app.route('/api/subscriptions/user/<int:user_id>', methods=['GET'])
def get_user_subscriptions(user_id):
    """
    Get user's subscriptions
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: List of subscriptions
    """
    subscriptions = data_persistence.get_user_subscriptions(user_id)
    return jsonify(subscriptions)

@app.route('/api/messages/send-bulk', methods=['POST'])
def send_bulk_messages():
    """
    Send bulk SMS messages
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - message
            - phone_numbers
          properties:
            message:
              type: string
              description: Message content
            phone_numbers:
              type: array
              items:
                type: string
              description: List of phone numbers
    responses:
      200:
        description: Bulk send results
      400:
        description: Validation error
    """
    import messaging
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    message = data.get('message')
    phone_numbers = data.get('phone_numbers')
    
    if not message or not phone_numbers:
        return jsonify({'error': 'message e phone_numbers são obrigatórios'}), 400
    
    if not isinstance(phone_numbers, list):
        return jsonify({'error': 'phone_numbers deve ser uma lista'}), 400
    
    results = messaging.send_bulk_sms(message, phone_numbers)
    
    return jsonify(results), 200

@app.route('/webhook/sms', methods=['POST'])
def webhook_sms():
    """
    Twilio SMS webhook endpoint
    ---
    parameters:
      - name: From
        in: formData
        type: string
        description: Sender phone number
      - name: Body
        in: formData
        type: string
        description: Message body
    responses:
      200:
        description: TwiML response
    """
    from command_handler import command_handler
    from twilio.twiml.messaging_response import MessagingResponse
    
    # Get message details
    from_number = request.form.get('From', '')
    message_body = request.form.get('Body', '')
    
    logging.info(f"SMS received from {from_number}: {message_body}")
    
    # Process command
    response_text = command_handler.process_message(from_number, message_body, channel='sms')
    
    # Create TwiML response
    resp = MessagingResponse()
    resp.message(response_text)
    
    return str(resp), 200, {'Content-Type': 'application/xml'}

@app.route('/webhook/whatsapp', methods=['POST'])
def webhook_whatsapp():
    """
    Twilio WhatsApp webhook endpoint
    ---
    parameters:
      - name: From
        in: formData
        type: string
        description: Sender phone number (whatsapp:+...)
      - name: Body
        in: formData
        type: string
        description: Message body
    responses:
      200:
        description: TwiML response
    """
    from command_handler import command_handler
    from twilio.twiml.messaging_response import MessagingResponse
    
    # Get message details
    from_number = request.form.get('From', '').replace('whatsapp:', '')
    message_body = request.form.get('Body', '')
    
    logging.info(f"WhatsApp received from {from_number}: {message_body}")
    
    # Process command
    response_text = command_handler.process_message(from_number, message_body, channel='wpp')
    
    # Create TwiML response
    resp = MessagingResponse()
    resp.message(response_text)
    
    return str(resp), 200, {'Content-Type': 'application/xml'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
