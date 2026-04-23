from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

# Carregado do .env — nunca expor diretamente no código
SECRET_KEY = config('SECRET_KEY')

# Em produção definir como False no .env
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []


# Apps nativos do Django + bibliotecas externas + apps do projeto
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # API REST
    'gestao',          # app principal do RACK+
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # pasta global de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',  # necessário para mensagens de feedback
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Todas as credenciais lidas do .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',  # suporte a acentos e caracteres especiais
        },
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Idioma e fuso horário
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True  # armazena em UTC no banco, converte para TIME_ZONE na exibição


STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # pasta global de estáticos


# Redirecionamentos do sistema de autenticação
LOGIN_REDIRECT_URL = 'gestao:home'
LOGIN_URL = '/login/'


# Configurações padrão da API REST
REST_FRAMEWORK = {
    # 1. QUEM PODE ACESSAR A API (Permissões)
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', # Exige autenticação para acessar qualquer endpoint da API
    ],
    
    # 2. COMO AUTENTICAR (Mecanismos)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',   # Permite autenticação via API (ex: Postman)
        'rest_framework.authentication.SessionAuthentication', # Permite autenticação via sessão (navegador)
    ],
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'