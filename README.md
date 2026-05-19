# 🐻 Capivara

> **Organize suas finanças de forma simples, prática e contínua!**

## 📊 Sobre o Projeto

**Capivara** é uma plataforma desenvolvida com o objetivo de auxiliar no controle financeiro pessoal, promovendo organização, disciplina e educação financeira de forma acessível.

O sistema foi projetado para ajudar usuários no acompanhamento de gastos, receitas, utilização de crédito e planejamento financeiro, oferecendo ferramentas que incentivam hábitos mais conscientes no dia a dia.

A proposta surgiu da dificuldade enfrentada por grande parte da população brasileira em manter uma organização financeira consistente, especialmente entre jovens adultos que iniciam a vida financeira sem acesso prévio à educação financeira estruturada.

Além do controle financeiro, o projeto busca reduzir o risco de endividamento, melhorar a previsibilidade financeira e incentivar decisões mais responsáveis relacionadas ao consumo e planejamento futuro.

Este projeto foi desenvolvido como parte do curso de **Ciência da Computação**.

---

## 🎯 Objetivos

- Facilitar o controle de gastos e receitas
- Incentivar hábitos financeiros mais conscientes
- Auxiliar no planejamento financeiro pessoal
- Reduzir riscos de endividamento
- Promover educação financeira de forma acessível
- Demonstrar a aplicação prática de conceitos de desenvolvimento web e banco de dados

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django**
- **PostgreSQL**

### Frontend
- **ChartJS**
- **Vite**
- **Sass**
- **Bootstrap**

### Funcionalidades
- Modularização de Importações
- Sistema de autenticação
- Criptografia de senhas
- Cache de dados para renderização otimizada

---

## ⚙️ Funcionalidades do Sistema

- Sistema de Autenticação de Usuários
- Tela de Gestão Financeira
- Tela de Dashboard
- Tela de Relatórios
- Gestão de registros

---

## 🌐 Páginas e Rotas Principais

- `home/`
- `dashboard/`
- `reports/`
- `calc/`
- `user/`
- `settings/`
- `register/`
- `login/`
- `login/esquecisenha/`
- `api/`

---

## 🚀 Como Executar o Projeto

### 1️⃣ Criar e ativar o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows
```

---

### 2️⃣ Instalar as dependências do Python

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Instalar as dependências do Frontend

```bash
# libs/frontend
npm install
```

---

### 4️⃣ Configurar o Banco de Dados (PostgreSQL)

- Crie um banco de dados no PostgreSQL.
- Importe o arquivo de banco de dados fornecido, localizado em `bd/bd.sql` (contendo a estrutura e os dados).
- A importação pode ser feita utilizando o **PgAdmin** através da opção *Restore*.

---

### 5️⃣ Configurar variáveis de ambiente

- Renomear o arquivo `.env.development` para `.env`
- Preencher as informações de conexão com o PostgreSQL

#### 🔐 Gerar a chave `RECOVERY_KEY`

A chave deve seguir o padrão exigido pelo **Fernet** (32 bytes codificados em base64).

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

### 6️⃣ Executar o projeto

```bash
python manage.py runserver
```

A aplicação estará disponível em:

```
http://127.0.0.1:8000
```

---

### 7️⃣ Modo Desenvolvimento

### Habilitar DEBUG

No arquivo `.env`, alterar:

```env
DEBUG=FALSE
```

para:

```env
DEBUG=TRUE
```

---

### Habilitar modo desenvolvimento do Vite

Nos arquivos `settings.py` e `production.py`, alterar:

```python
DJANGO_VITE = {
    "default": {
        "dev_mode": False,
    }
}
```

para:

```python
DJANGO_VITE = {
    "default": {
        "dev_mode": True,
    }
}
```

---

### Executar servidor do Vite

Entrar no diretório:

```bash
libs/frontend
```

Executar:

```bash
npm run dev
```

---

### Adicionar novos ícones

1. Adicionar o arquivo em:

```text
static/icons
```

2. Registrar o ícone em:

```text
static/css/icons.scss
```

3. Executar no diretório `libs/frontend`:

```bash
npm run build:icons
```

---

### Configuração básica do Nginx

#### Instalação

```bash
sudo apt update
sudo apt install nginx
```

#### Configuração

Criar o arquivo:

```bash
/etc/nginx/sites-available/projeto
```

Conteúdo:

```nginx
server {
    listen 8000;
    server_name localhost;

    location /static/ {
        alias {pasta onde o projeto está}/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Habilitar configuração:

```bash
sudo ln -s /etc/nginx/sites-available/projeto /etc/nginx/sites-enabled/
```

Validar:

```bash
sudo nginx -t
```

Reiniciar:

```bash
sudo systemctl restart nginx
```

---

## 📌 Status do Projeto

🎓 **Projeto acadêmico finalizado**, com margem para melhorias e novas funcionalidades.

---

## 🔗 Links

- Repositório GitHub: https://github.com/luizbenedito-netizen/capivara

---

## 👤 Autor

**Luiz Otávio de P. B.**  
Curso: Ciência da Computação  
Instituição: IFSULDEMINAS – Campus Muzambinho  
GitHub: https://github.com/luizbenedito-netizen

---

## 📄 Licença

Este projeto é destinado exclusivamente para **uso acadêmico**.

