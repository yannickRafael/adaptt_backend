# Gunicorn Production Deployment Guide - AWS EC2

## Step 1: Install Gunicorn

```bash
cd ~/adaptt_backend
source venv/bin/activate
pip install gunicorn
pip freeze > requirements.txt
```

## Step 2: Create Gunicorn Configuration

Create `gunicorn_config.py`:

```python
# gunicorn_config.py
import multiprocessing

# Server socket
bind = "0.0.0.0:5001"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/home/ubuntu/adaptt_backend/logs/gunicorn-access.log"
errorlog = "/home/ubuntu/adaptt_backend/logs/gunicorn-error.log"
loglevel = "info"

# Process naming
proc_name = "adaptt_backend"

# Server mechanics
daemon = False
pidfile = "/home/ubuntu/adaptt_backend/gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
```

## Step 3: Create Logs Directory

```bash
mkdir -p ~/adaptt_backend/logs
```

## Step 4: Create Systemd Service

Create `/etc/systemd/system/adaptt.service`:

```bash
sudo nano /etc/systemd/system/adaptt.service
```

Add this content:

```ini
[Unit]
Description=ADAPTT Backend Gunicorn Service
After=network.target

[Service]
Type=notify
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/adaptt_backend
Environment="PATH=/home/ubuntu/adaptt_backend/venv/bin"
ExecStart=/home/ubuntu/adaptt_backend/venv/bin/gunicorn \
    --config /home/ubuntu/adaptt_backend/gunicorn_config.py \
    app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Step 5: Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable adaptt

# Start service
sudo systemctl start adaptt

# Check status
sudo systemctl status adaptt
```

## Step 6: Useful Commands

```bash
# View logs
sudo journalctl -u adaptt -f

# Restart service
sudo systemctl restart adaptt

# Stop service
sudo systemctl stop adaptt

# Check if running
sudo systemctl status adaptt

# View Gunicorn logs
tail -f ~/adaptt_backend/logs/gunicorn-access.log
tail -f ~/adaptt_backend/logs/gunicorn-error.log
```

## Step 7: Configure Nginx (Recommended)

Install Nginx:
```bash
sudo apt update
sudo apt install nginx -y
```

Create Nginx config `/etc/nginx/sites-available/adaptt`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # or EC2 public IP

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeout for long-running requests
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Webhook endpoints
    location /webhook/ {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable Nginx site:
```bash
sudo ln -s /etc/nginx/sites-available/adaptt /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 8: Configure Firewall

```bash
# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS (if using SSL)
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

## Step 9: Update Twilio Webhooks

Update your Twilio webhooks to use your EC2 public IP or domain:

- SMS: `http://your-ec2-ip/webhook/sms`
- WhatsApp: `http://your-ec2-ip/webhook/whatsapp`

Or with domain:
- SMS: `http://your-domain.com/webhook/sms`
- WhatsApp: `http://your-domain.com/webhook/whatsapp`

## Step 10: SSL with Let's Encrypt (Optional but Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

## Monitoring

### Check if Gunicorn is running:
```bash
ps aux | grep gunicorn
```

### Check port usage:
```bash
sudo netstat -tulpn | grep 5001
```

### Monitor system resources:
```bash
htop
```

## Troubleshooting

### Service won't start:
```bash
# Check logs
sudo journalctl -u adaptt -n 50 --no-pager

# Check permissions
ls -la /home/ubuntu/adaptt_backend

# Test Gunicorn manually
cd ~/adaptt_backend
source venv/bin/activate
gunicorn --config gunicorn_config.py app:app
```

### Port already in use:
```bash
# Find process using port 5001
sudo lsof -i :5001

# Kill process
sudo kill -9 <PID>
```

### Webhooks not working:
```bash
# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Check Gunicorn logs
tail -f ~/adaptt_backend/logs/gunicorn-error.log
```

## Performance Tuning

### Adjust workers based on CPU:
```python
# In gunicorn_config.py
workers = (2 * cpu_count) + 1  # General recommendation
```

### For high traffic:
```python
worker_class = "gevent"  # Async workers
workers = 4
worker_connections = 1000
```

## Deployment Checklist

- [ ] Gunicorn installed
- [ ] gunicorn_config.py created
- [ ] Logs directory created
- [ ] Systemd service created
- [ ] Service enabled and started
- [ ] Nginx installed and configured
- [ ] Firewall configured
- [ ] Twilio webhooks updated
- [ ] SSL certificate installed (optional)
- [ ] Monitoring set up

## Quick Start Commands

```bash
# One-time setup
cd ~/adaptt_backend
source venv/bin/activate
pip install gunicorn
mkdir -p logs

# Create and start service
sudo systemctl daemon-reload
sudo systemctl enable adaptt
sudo systemctl start adaptt

# Check status
sudo systemctl status adaptt
```

Your Flask app is now running in production with Gunicorn! 🚀
