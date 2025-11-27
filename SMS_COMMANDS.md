# Sistema de Comandos SMS/WhatsApp

## Comandos Disponíveis

### 1. REGISTRAR [Nome] [Região]
Cria uma conta de usuário.

**Exemplo:**
```
REGISTRAR João Silva maputo
```

**Resposta:**
```
✅ Bem-vindo, João Silva! Conta criada com sucesso.

Envie LISTAR para ver projetos disponíveis.
```

**Regiões válidas:**
- maputo
- maputo-city
- gaza
- inhambane
- sofala
- manica
- tete
- zambezia
- nampula
- cabo-delgado
- niassa

---

### 2. LISTAR
Mostra projetos disponíveis para subscrição.

**Exemplo:**
```
LISTAR
```

**Resposta:**
```
📋 PROJETOS DISPONÍVEIS:

1. Manutenção Periódica de Estradas
   ID: 9oFiIdSZv4Ruc2SdaVWQ
   Score: 0 (RED)

2. PROMOVE Transporte
   ID: F2k34immfcN5X14KZywa
   Score: 0 (RED)

Para subscrever: SUBSCREVER [ID]
```

---

### 3. SUBSCREVER [ID_Projeto] [sms|wpp]
Subscreve a um projeto para receber alertas.

**Exemplos:**
```
SUBSCREVER 9oFiIdSZv4Ruc2SdaVWQ wpp
SUBSCREVER F2k34immfcN5X14KZywa sms
SUBSCREVER abc123
```

**Resposta:**
```
✅ Subscrito com sucesso!

Você receberá alertas por WhatsApp sobre mudanças no projeto.
```

---

### 4. CANCELAR [ID_Projeto]
Cancela subscrição a um projeto.

**Exemplo:**
```
CANCELAR 9oFiIdSZv4Ruc2SdaVWQ
```

**Resposta:**
```
✅ Subscrição cancelada com sucesso.
```

---

### 5. AJUDA
Mostra lista de comandos.

**Exemplo:**
```
AJUDA
```

---

## Configuração Twilio

### 1. Configurar Webhooks

Acesse Twilio Console e configure:

**Para SMS:**
- Phone Numbers → Active Numbers → Seu número
- Messaging → Configure
- A MESSAGE COMES IN: `https://seu-dominio.com/webhook/sms`

**Para WhatsApp:**
- Messaging → Try it out → WhatsApp sandbox
- WHEN A MESSAGE COMES IN: `https://seu-dominio.com/webhook/whatsapp`

### 2. Expor Servidor Localmente (Desenvolvimento)

Use ngrok para expor localhost:

```bash
ngrok http 5001
```

Copie a URL (ex: `https://abc123.ngrok.io`) e use nos webhooks:
- `https://abc123.ngrok.io/webhook/sms`
- `https://abc123.ngrok.io/webhook/whatsapp`

---

## Fluxo de Uso

### Novo Usuário

1. **Registrar:**
   ```
   REGISTRAR Maria Santos gaza
   ```

2. **Ver Projetos:**
   ```
   LISTAR
   ```

3. **Subscrever:**
   ```
   SUBSCREVER abc123 wpp
   ```

4. **Receber Alertas:**
   - Sistema envia automaticamente quando prazo muda

### Cancelar Subscrição

```
CANCELAR abc123
```

---

## Logs

Todas as interações são registradas:
```python
logging.info(f"SMS received from {phone_number}: {message_body}")
```

Verifique logs para debug.

---

## Testes

### Teste Manual via SMS
Envie SMS para seu número Twilio com comandos.

### Teste via API (Simular Webhook)
```bash
curl -X POST http://localhost:5001/webhook/sms \
  -d "From=+258844236139" \
  -d "Body=AJUDA"
```

---

## Notas Importantes

- Comandos não são case-sensitive
- Número de telefone é usado como identificador único
- Canal padrão é o mesmo da mensagem recebida
- Máximo 5 projetos por resposta LISTAR
