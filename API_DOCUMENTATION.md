# Documentação da API ADAPTT

Este documento descreve como utilizar a API do ADAPTT (Backend) e como interagir com o arquivo `swagger.yaml`.

## 📄 Arquivo Swagger (`swagger.yaml`)

O arquivo `swagger.yaml` contém a definição completa da API seguindo a especificação OpenAPI 2.0 (Swagger). Ele descreve:
- Todos os endpoints disponíveis
- Parâmetros de entrada (body, path, query)
- Estrutura das respostas
- Modelos de dados

### Como visualizar a documentação interativa

1. **Via Swagger Editor (Online):**
   - Acesse [editor.swagger.io](https://editor.swagger.io/)
   - Copie o conteúdo de `swagger.yaml`
   - Cole no editor para ver a documentação visual

2. **Via VS Code:**
   - Instale a extensão "OpenAPI (Swagger) Editor"
   - Abra o arquivo `swagger.yaml`
   - Clique no ícone de preview

3. **Via Aplicação (Flasgger):**
   - Com o servidor rodando (`python app.py`), acesse:
   - `http://localhost:5001/apidocs/`

---

## 🚀 Guia de Uso da API

### Base URL
- **Desenvolvimento:** `http://localhost:5001`
- **Produção:** `http://seu-servidor-ip:5001` (ou seu domínio)

### 1. Consultar Projetos

**Listar todos os projetos:**
```http
GET /api/projects
```

**Ver detalhes de um projeto:**
```http
GET /api/projects/{project_id}
```

**Ver documentos de um projeto:**
```http
GET /api/projects/{project_id}/documents
```

### 2. Gestão de Usuários

**Registrar novo usuário:**
```http
POST /api/users/register
Content-Type: application/json

{
  "name": "Maria Santos",
  "phone_number": "+258841234567",
  "region_id": "maputo"
}
```

### 3. Subscrições

**Subscrever a um projeto:**
```http
POST /api/subscriptions
Content-Type: application/json

{
  "user_id": 1,
  "project_id": "abc12345",
  "notification_channel": "wpp"  // ou "sms"
}
```

**Ver minhas subscrições:**
```http
GET /api/subscriptions/user/{user_id}
```

**Cancelar subscrição:**
```http
DELETE /api/subscriptions
Content-Type: application/json

{
  "user_id": 1,
  "project_id": "abc12345"
}
```

### 4. Webhooks (Twilio)

Estes endpoints são chamados automaticamente pelo Twilio quando uma mensagem é recebida.

- **SMS:** `POST /webhook/sms`
- **WhatsApp:** `POST /webhook/whatsapp`

Eles esperam dados no formato `application/x-www-form-urlencoded` (padrão do Twilio) e retornam XML (TwiML).

---

## 🛠️ Ferramentas Recomendadas

- **Postman / Insomnia:** Para testar requisições manualmente.
- **curl:** Para testes rápidos via terminal.

**Exemplo com curl:**
```bash
curl -X GET http://localhost:5001/api/projects
```
