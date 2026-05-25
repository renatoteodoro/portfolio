# Portfolio - Renato Teodoro

Portfolio profissional de desenvolvedor Python, com foco em Django, IA e IoT.

## Tecnologias

- Python 3.11+
- Django 5.x
- Tailwind CSS (CDN)
- Font Awesome
- WhiteNoise (static files)
- python-decouple (configuração por ambiente)

## Instalação Local

### 1. Clone o repositório

```bash
git clone https://github.com/[seu-usuario]/portfolio.git
cd portfolio
```

### 2. Crie e ative o ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações reais
```

### 5. Execute as migrations

```bash
python manage.py migrate
```

### 6. Colete arquivos estáticos (produção)

```bash
python manage.py collectstatic
```

### 7. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

---

## Deploy no Railway

### 1. Crie uma conta em [railway.app](https://railway.app)

### 2. Instale a CLI do Railway

```bash
npm install -g @railway/cli
railway login
```

### 3. Inicialize e suba o projeto

```bash
railway init
railway up
```

### 4. Configure as variáveis de ambiente no painel Railway

| Variável | Valor |
|---|---|
| `SECRET_KEY` | Chave secreta Django (gere uma nova) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `seu-app.railway.app` |
| `EMAIL_HOST_USER` | Seu email Gmail |
| `EMAIL_HOST_PASSWORD` | Senha de app Gmail |

### Gerar uma SECRET_KEY segura

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Deploy no Render

### 1. Crie uma conta em [render.com](https://render.com)

### 2. Conecte seu repositório GitHub

### 3. Crie um novo Web Service com as configurações:

- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command**: `gunicorn portfolio.wsgi --log-file -`

### 4. Adicione as variáveis de ambiente no painel Render

---

## Configurando Email (Gmail)

1. Ative a verificação em duas etapas na sua conta Google
2. Acesse: Google Account > Seguranca > Senhas de app
3. Gere uma senha de app para "Email"
4. Use essa senha no `EMAIL_HOST_PASSWORD`

---

## Estrutura do Projeto

```
portfolio/
├── manage.py
├── requirements.txt
├── Procfile
├── .env.example
├── .gitignore
├── README.md
├── portfolio/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/
    ├── __init__.py
    ├── apps.py
    ├── urls.py
    ├── views.py
    └── templates/
        └── core/
            ├── base.html
            ├── index.html
            └── projeto_detail.html
```

---

## Licenca

MIT License - veja o arquivo LICENSE para detalhes.
