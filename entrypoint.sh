#!/bin/bash
set -e

# Configuração Nginx
mkdir -p /etc/nginx/sites-available
cat > /etc/nginx/sites-available/app <<EOL
server {
    listen 8000;
    server_name localhost;

    location /static/ {
        alias /app/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL

ln -sf /etc/nginx/sites-available/app /etc/nginx/sites-enabled/app

# Configuração Cloudflare Tunnel
mkdir -p /etc/cloudflared
cat > /etc/cloudflared/config.yml <<EOL
tunnel: django-tunnel
token: $CLOUDFLARE_TUNNEL_TOKEN
ingress:
  - hostname: $CLOUDFLARE_HOSTNAME
    service: http://127.0.0.1:8000
  - hostname: www.$CLOUDFLARE_HOSTNAME
    service: http://127.0.0.1:8000
  - service: http_status:404
EOL

# Migrates e coleta estáticos
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Corrige permissões de staticfiles
if [ -d "/app/staticfiles" ]; then
    chmod -R 755 /app/staticfiles
fi

# Inicia Nginx em background
nginx -g 'daemon off;' &

# Inicia Cloudflare Tunnel em background
cloudflared tunnel run --token "$CLOUDFLARE_TUNNEL_TOKEN" &

# Inicia Gunicorn em primeiro plano
GUNICORN_ARGS="
  --bind 127.0.0.1:8001
  --workers 3
  --log-level info
"

if [ "$AUTO_RELOAD" = "true" ]; then
  GUNICORN_ARGS="$GUNICORN_ARGS --reload"
fi

exec gunicorn config.wsgi:application $GUNICORN_ARGS