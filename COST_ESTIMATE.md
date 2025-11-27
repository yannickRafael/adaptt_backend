# Estimativa de Custos - Projeto ADAPTT

## Resumo Executivo

**Custo Mensal Total Estimado: $85 - $165 USD/mês**
**Custo Anual Estimado: $1,020 - $1,980 USD/ano**

---

## 1. Infraestrutura Backend (AWS EC2)

### Opção 1: Ambiente de Produção Pequeno
**Instância: t3.small**
- vCPUs: 2
- RAM: 2 GB
- Armazenamento: 20 GB SSD
- Tráfego: ~100 GB/mês

**Custo Mensal:**
- Instância EC2 (t3.small): $15.18/mês
- Armazenamento EBS (20 GB): $2.00/mês
- Transferência de dados (100 GB): $9.00/mês
- IP Elástico: $3.60/mês (se não usado 100% do tempo)
- **Subtotal: ~$30/mês**

### Opção 2: Ambiente de Produção Médio (Recomendado)
**Instância: t3.medium**
- vCPUs: 2
- RAM: 4 GB
- Armazenamento: 30 GB SSD
- Tráfego: ~200 GB/mês

**Custo Mensal:**
- Instância EC2 (t3.medium): $30.37/mês
- Armazenamento EBS (30 GB): $3.00/mês
- Transferência de dados (200 GB): $18.00/mês
- IP Elástico: $3.60/mês
- **Subtotal: ~$55/mês**

### Opção 3: Alta Disponibilidade
**2x t3.small + Load Balancer**
- 2 instâncias para redundância
- Application Load Balancer
- Auto-scaling configurado

**Custo Mensal:**
- 2x Instâncias EC2 (t3.small): $30.36/mês
- Load Balancer: $16.20/mês
- Armazenamento EBS (40 GB total): $4.00/mês
- Transferência de dados (200 GB): $18.00/mês
- **Subtotal: ~$68/mês**

---

## 2. Frontend (Vercel)

### Plano Hobby (Gratuito)
**Limitações:**
- 100 GB bandwidth/mês
- Builds ilimitados
- Domínio personalizado
- SSL automático
- **Custo: $0/mês**

**Adequado para:**
- Fase inicial/MVP
- Até ~10,000 visitantes/mês
- Projetos não-comerciais

### Plano Pro (Recomendado para Produção)
**Recursos:**
- 1 TB bandwidth/mês
- Builds mais rápidos
- Suporte prioritário
- Analytics avançado
- Proteção DDoS
- **Custo: $20/mês por membro**

**Adequado para:**
- Produção
- Até ~100,000 visitantes/mês
- Aplicações comerciais

---

## 3. Serviços Twilio (SMS/WhatsApp)

### SMS
**Preços Moçambique:**
- Envio: $0.0531 por SMS
- Recebimento: $0.0075 por SMS

**Estimativa Mensal:**
- 500 SMS enviados: $26.55
- 500 SMS recebidos: $3.75
- **Subtotal SMS: ~$30/mês**

### WhatsApp Business API
**Preços:**
- Conversas iniciadas pelo negócio: $0.0160 por conversa
- Conversas iniciadas pelo usuário: $0.0080 por conversa
- Primeiras 1,000 conversas/mês: GRÁTIS

**Estimativa Mensal (após 1,000 gratuitas):**
- 500 conversas adicionais: $8.00
- **Subtotal WhatsApp: ~$8/mês**

### Número Twilio
- Número de telefone: $1.00/mês
- **Subtotal: $1/mês**

**Total Twilio: ~$39/mês** (com uso moderado)

---

## 4. Domínio e SSL

### Domínio
- Registro .com ou .mz: $12-15/ano
- **Custo Mensal: ~$1.25/mês**

### SSL Certificate
- Let's Encrypt: **GRÁTIS**
- Ou incluído no Vercel: **GRÁTIS**

---

## 5. Serviços Adicionais (Opcionais)

### Monitoramento
- **UptimeRobot** (básico): GRÁTIS
- **New Relic** (APM): $25-99/mês
- **Datadog** (monitoring): $15-31/mês

### Backup
- **AWS S3** para backups: $1-5/mês
- **Automated backups**: Incluído no EC2

### Email Transacional (se necessário)
- **SendGrid** (free tier): 100 emails/dia GRÁTIS
- **Mailgun**: $0.80/1000 emails

---

## Cenários de Custo

### Cenário 1: MVP / Fase Inicial
**Componentes:**
- EC2 t3.small: $30/mês
- Vercel Hobby: $0/mês
- Twilio (uso baixo): $20/mês
- Domínio: $1.25/mês
- **Total: ~$51/mês ($612/ano)**

**Adequado para:**
- Lançamento inicial
- Até 1,000 usuários
- 200-300 mensagens/mês

---

### Cenário 2: Produção Padrão (Recomendado)
**Componentes:**
- EC2 t3.medium: $55/mês
- Vercel Pro: $20/mês
- Twilio (uso moderado): $39/mês
- Domínio: $1.25/mês
- Monitoramento básico: $0/mês
- **Total: ~$115/mês ($1,380/ano)**

**Adequado para:**
- Produção estável
- 5,000-10,000 usuários
- 500-1,000 mensagens/mês

---

### Cenário 3: Alta Demanda
**Componentes:**
- EC2 com Load Balancer: $68/mês
- Vercel Pro: $20/mês
- Twilio (uso alto): $80/mês
- Domínio: $1.25/mês
- Monitoramento (New Relic): $25/mês
- Backup S3: $5/mês
- **Total: ~$199/mês ($2,388/ano)**

**Adequado para:**
- Alto tráfego
- 20,000+ usuários
- 2,000+ mensagens/mês
- Necessidade de alta disponibilidade

---

## Otimizações de Custo

### 1. AWS Reserved Instances
- Economize até 72% com compromisso de 1-3 anos
- t3.medium: $30/mês → $18/mês (1 ano)
- **Economia: $144/ano**

### 2. Twilio
- Use WhatsApp em vez de SMS (mais barato)
- Aproveite 1,000 conversas WhatsApp gratuitas/mês
- **Economia potencial: $20-30/mês**

### 3. Vercel
- Comece com plano Hobby (grátis)
- Upgrade apenas quando necessário
- **Economia inicial: $20/mês**

### 4. Transferência de Dados
- Use CloudFront CDN para reduzir custos
- Comprima imagens e assets
- **Economia: $5-10/mês**

---

## Projeção de Crescimento

### Ano 1 (Lançamento)
- Meses 1-3: Cenário MVP (~$51/mês)
- Meses 4-12: Cenário Produção (~$115/mês)
- **Custo Ano 1: ~$1,188**

### Ano 2 (Crescimento)
- Cenário Produção estável
- Possível upgrade para alta demanda
- **Custo Ano 2: ~$1,380-1,800**

### Ano 3+ (Escala)
- Alta demanda com otimizações
- Reserved Instances aplicadas
- **Custo Ano 3+: ~$1,500-2,000**

---

## Custos Não-Recorrentes

### Desenvolvimento
- Frontend (React/Next.js): 80-120 horas
- Testes e QA: 20-40 horas
- Design UI/UX: 40-60 horas
- **Estimativa: $8,000-15,000** (se terceirizado)

### Setup Inicial
- Configuração AWS: 4-8 horas
- Configuração Twilio: 2-4 horas
- Deploy e CI/CD: 4-8 horas
- **Estimativa: $500-1,000** (se terceirizado)

---

## Comparação com Alternativas

### Backend Alternativo: Heroku
- Dyno Standard-1X: $25/mês
- Postgres Basic: $9/mês
- **Total: $34/mês** (mais barato, mas menos controle)

### Backend Alternativo: DigitalOcean
- Droplet 2GB: $18/mês
- **Total: $18/mês** (mais barato que AWS)

### Frontend Alternativo: Netlify
- Starter: $0/mês
- Pro: $19/mês
- **Similar ao Vercel**

---

## Recomendação Final

### Para Começar (Meses 1-3)
**Custo: ~$51/mês**
- EC2 t3.small
- Vercel Hobby (grátis)
- Twilio básico
- Total investimento inicial: ~$153 (3 meses)

### Para Produção (Meses 4+)
**Custo: ~$115/mês**
- EC2 t3.medium
- Vercel Pro
- Twilio moderado
- Total anual: ~$1,380

### Orçamento Recomendado
- **Ano 1**: $1,200-1,500
- **Anos seguintes**: $1,400-1,800
- **Buffer para crescimento**: +20%

---

## Notas Importantes

1. **Custos variáveis**: Twilio depende do uso real
2. **Picos de tráfego**: Considere auto-scaling
3. **Backup**: Sempre inclua no orçamento
4. **Monitoramento**: Essencial para produção
5. **Suporte**: Considere planos de suporte AWS/Vercel

---

## Checklist de Custos

- [ ] Servidor backend (EC2)
- [ ] Armazenamento e backup
- [ ] Transferência de dados
- [ ] Frontend hosting (Vercel)
- [ ] SMS/WhatsApp (Twilio)
- [ ] Domínio
- [ ] SSL (grátis)
- [ ] Monitoramento
- [ ] Margem para crescimento (20%)

---

**Última atualização:** Novembro 2025
**Preços baseados em:** AWS us-east-1, Twilio Moçambique, Vercel USD
