import re
import logging
import data_persistence

class CommandHandler:
    """Handles SMS/WhatsApp commands for user interaction."""
    
    def __init__(self):
        self.commands = {
            'REGISTRAR': self.handle_registrar,
            'LISTAR': self.handle_listar,
            'SUBSCREVER': self.handle_subscrever,
            'CANCELAR': self.handle_cancelar,
            'AJUDA': self.handle_ajuda,
            'HELP': self.handle_ajuda
        }
    
    def process_message(self, phone_number, message_body, channel='sms'):
        """
        Processes incoming message and returns response.
        
        Args:
            phone_number: Sender's phone number
            message_body: Message text
            channel: 'sms' or 'wpp'
        
        Returns: Response message string
        """
        try:
            # Normalize message
            message = message_body.strip().upper()
            
            # Parse command
            parts = message.split(maxsplit=1)
            if not parts:
                return self.handle_ajuda()
            
            command = parts[0]
            args = parts[1] if len(parts) > 1 else ''
            
            # Execute command
            if command in self.commands:
                return self.commands[command](phone_number, args, channel)
            else:
                return f"❌ Comando '{command}' não reconhecido. Envie AJUDA para ver comandos disponíveis."
        
        except Exception as e:
            logging.error(f"Error processing command from {phone_number}: {e}")
            return "❌ Erro ao processar comando. Tente novamente ou envie AJUDA."
    
    def handle_registrar(self, phone_number, args, channel):
        """Handle REGISTRAR [Nome] [Região]"""
        try:
            # Parse: REGISTRAR João Silva maputo
            match = re.match(r'^(.+?)\s+(\S+)$', args, re.IGNORECASE)
            if not match:
                return "❌ Formato incorreto. Use: REGISTRAR [Nome Completo] [Região]\nExemplo: REGISTRAR João Silva maputo"
            
            name = match.group(1).strip()
            region_id = match.group(2).strip().lower()
            
            # Validate region
            if not data_persistence.region_exists(region_id):
                return f"❌ Região '{region_id}' não existe. Use: maputo, gaza, inhambane, sofala, manica, tete, zambezia, nampula, cabo-delgado, niassa, maputo-city"
            
            # Check if user already exists
            existing = data_persistence.get_user_by_phone(phone_number)
            if existing:
                return f"ℹ️ Você já está registrado como '{existing['name']}'. Use LISTAR para ver projetos."
            
            # Register user
            success, message, user_id = data_persistence.register_user(name, phone_number, region_id)
            
            if success:
                return f"✅ Bem-vindo, {name}! Conta criada com sucesso.\n\nEnvie LISTAR para ver projetos disponíveis."
            else:
                return f"❌ {message}"
        
        except Exception as e:
            logging.error(f"Error in handle_registrar: {e}")
            return "❌ Erro ao registrar. Verifique o formato e tente novamente."
    
    def handle_listar(self, phone_number, args, channel):
        """Handle LISTAR"""
        try:
            # Check if user exists
            user = data_persistence.get_user_by_phone(phone_number)
            if not user:
                return "❌ Você precisa se registrar primeiro. Use: REGISTRAR [Nome] [Região]"
            
            # Get projects
            projects = data_persistence.get_all_projects()
            
            if not projects:
                return "ℹ️ Nenhum projeto disponível no momento."
            
            # Format response (limit to 5 projects)
            response = "📋 PROJETOS DISPONÍVEIS:\n\n"
            for i, project in enumerate(projects[:5], 1):
                score = project.get('transparency_score', 'N/A')
                alert = project.get('alert_color', 'N/A')
                response += f"{i}. {project['project_name']}\n"
                response += f"   ID: {project['project_id']}\n"
                response += f"   Score: {score} ({alert})\n\n"
            
            if len(projects) > 5:
                response += f"... e mais {len(projects) - 5} projetos.\n\n"
            
            response += "Para subscrever: SUBSCREVER [ID]"
            return response
        
        except Exception as e:
            logging.error(f"Error in handle_listar: {e}")
            return "❌ Erro ao listar projetos."
    
    def handle_subscrever(self, phone_number, args, channel):
        """Handle SUBSCREVER [ID_Projeto] [sms|wpp]"""
        try:
            # Check if user exists
            user = data_persistence.get_user_by_phone(phone_number)
            if not user:
                return "❌ Você precisa se registrar primeiro. Use: REGISTRAR [Nome] [Região]"
            
            # Parse arguments
            parts = args.split()
            if not parts:
                return "❌ Formato incorreto. Use: SUBSCREVER [ID_Projeto] [sms|wpp]\nExemplo: SUBSCREVER abc123 wpp"
            
            project_id = parts[0]
            notification_channel = parts[1].lower() if len(parts) > 1 else channel
            
            # Validate channel
            if notification_channel not in ['sms', 'wpp']:
                notification_channel = channel
            
            # Subscribe
            success, message, sub_id = data_persistence.subscribe_to_project(
                user['user_id'], project_id, notification_channel
            )
            
            if success:
                channel_name = "WhatsApp" if notification_channel == 'wpp' else "SMS"
                return f"✅ Subscrito com sucesso!\n\nVocê receberá alertas por {channel_name} sobre mudanças no projeto."
            else:
                return f"❌ {message}"
        
        except Exception as e:
            logging.error(f"Error in handle_subscrever: {e}")
            return "❌ Erro ao subscrever."
    
    def handle_cancelar(self, phone_number, args, channel):
        """Handle CANCELAR [ID_Projeto]"""
        try:
            # Check if user exists
            user = data_persistence.get_user_by_phone(phone_number)
            if not user:
                return "❌ Você precisa se registrar primeiro."
            
            # Parse project ID
            project_id = args.strip()
            if not project_id:
                return "❌ Formato incorreto. Use: CANCELAR [ID_Projeto]\nExemplo: CANCELAR abc123"
            
            # Unsubscribe
            success, message = data_persistence.unsubscribe_from_project(user['user_id'], project_id)
            
            if success:
                return f"✅ {message}"
            else:
                return f"❌ {message}"
        
        except Exception as e:
            logging.error(f"Error in handle_cancelar: {e}")
            return "❌ Erro ao cancelar subscrição."
    
    def handle_ajuda(self, phone_number=None, args=None, channel=None):
        """Handle AJUDA"""
        return """📱 COMANDOS ADAPTT

REGISTRAR [Nome] [Região]
  Criar conta
  Ex: REGISTRAR João Silva maputo

LISTAR
  Ver projetos disponíveis

SUBSCREVER [ID] [sms|wpp]
  Subscrever a projeto
  Ex: SUBSCREVER abc123 wpp

CANCELAR [ID]
  Cancelar subscrição
  Ex: CANCELAR abc123

AJUDA
  Mostrar esta mensagem

ℹ️ Regiões: maputo, gaza, inhambane, sofala, manica, tete, zambezia, nampula, cabo-delgado, niassa, maputo-city"""

# Global handler instance
command_handler = CommandHandler()
