# Sistema de Monitoramento de Prazos - Guia de Uso

## Visão Geral
Sistema automático que detecta mudanças em prazos de projetos e notifica usuários subscritos via SMS/WhatsApp.

## Componentes

### 1. Tabela de Auditoria (`project_audit`)
Registra todos os eventos de mudança de prazo:
- `deadline_expired`: Prazo expirou
- `deadline_extended`: Prazo foi estendido
- `deadline_changed`: Prazo foi alterado

### 2. Detector de Mudanças (`deadline_monitor.py`)
- Compara dados antigos vs novos durante sincronização
- Detecta mudanças no campo `implementationPeriod.endDate`
- Registra eventos na tabela de auditoria

### 3. Worker de Notificações (`notification_worker.py`)
- Thread em background rodando a cada 30 segundos
- Monitora tabela `project_audit` para eventos não notificados
- Envia alertas para usuários subscritos

## Como Funciona

### Fluxo Automático
1. **Sincronização**: `main.py` executa sync de projetos
2. **Detecção**: Sistema compara dados e detecta mudanças
3. **Auditoria**: Eventos são registrados em `project_audit`
4. **Monitoramento**: Worker verifica novos eventos a cada 30s
5. **Notificação**: Envia SMS/WhatsApp para usuários subscritos

### Tipos de Notificação

**Prazo Expirado:**
```
ALERTA ADAPTT: O prazo do projeto 'Nome do Projeto' expirou em 2024-12-31. Verifique o status.
```

**Prazo Estendido:**
```
ATUALIZAÇÃO ADAPTT: O prazo do projeto 'Nome do Projeto' foi estendido de 2024-12-31 para 2025-06-30.
```

## Consultar Eventos de Auditoria

```sql
-- Ver todos os eventos
SELECT * FROM project_audit ORDER BY detected_at DESC;

-- Ver eventos não notificados
SELECT * FROM project_audit WHERE notified = 0;

-- Ver eventos por projeto
SELECT * FROM project_audit WHERE project_id = 'PROJECT_ID';
```

## Configuração

### Intervalo de Monitoramento
Edite `notification_worker.py`:
```python
notification_worker = NotificationWorker(check_interval=30)  # segundos
```

### Iniciar Worker Manualmente
```python
from notification_worker import notification_worker
notification_worker.start()
```

### Parar Worker
```python
notification_worker.stop()
```

## Logs
O sistema registra todas as ações:
- Eventos detectados
- Notificações enviadas
- Erros de envio

Verifique os logs para monitorar o funcionamento.
