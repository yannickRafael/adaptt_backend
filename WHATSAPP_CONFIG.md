# WhatsApp Configuration Guide

## Configuração Necessária

Adicione ao seu arquivo `.env`:

```bash
# WhatsApp Twilio
TWILIO_WHATSAPP_NUMBER=+14155238886
TWILIO_WHATSAPP_CONTENT_SID=HXb5b62575e6e4ff6129ad7c8efe1f983e
```

## Como Funciona

### 1. SMS (Texto Livre)
- Usa `send_single_sms()` 
- Envia mensagem de texto diretamente
- ✅ Já testado e funcionando

### 2. WhatsApp (Template Aprovado)
- Usa `send_whatsapp_message()` com `content_sid`
- Requer template aprovado pela Meta
- Variáveis são substituídas no template

## Estrutura do Template

Seu template `HXb5b62575e6e4ff6129ad7c8efe1f983e` espera variáveis:
- `{{1}}` = Data do prazo
- `{{2}}` = Nome do projeto

Exemplo de uso:
```python
messaging.send_whatsapp_message(
    message="Fallback text",
    phone_number="+258844236139",
    content_sid="HXb5b62575e6e4ff6129ad7c8efe1f983e",
    content_variables={"1": "2024-12-31", "2": "Projeto Exemplo"}
)
```

## Teste Manual

```bash
curl -X POST http://localhost:5001/api/messages/send-bulk \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Teste WhatsApp",
    "phone_numbers": ["+258844236139"]
  }'
```

## Notificações Automáticas

O sistema agora:
1. Detecta mudanças de prazo
2. Verifica canal de preferência do usuário (`sms` ou `wpp`)
3. Envia via SMS (texto livre) ou WhatsApp (template)

**Para WhatsApp:** As variáveis do template são preenchidas automaticamente:
- Variável 1: Data do prazo
- Variável 2: Nome do projeto

## Personalizar Template

Se seu template tiver estrutura diferente, edite `notification_worker.py`:

```python
def _prepare_whatsapp_variables(self, event):
    return {
        "1": "sua_variavel_1",
        "2": "sua_variavel_2",
        # ... adicione mais conforme necessário
    }
```
