# RACK+

Sistema web para gestão hierárquica de infraestrutura de rede e monitoramento de dispositivos organizados por **salas**, **racks** e **devices**.

---

## Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Objetivo do sistema](#objetivo-do-sistema)
- [Principais funcionalidades](#principais-funcionalidades)
- [Modelagem do domínio](#modelagem-do-domínio)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e configuração](#instalação-e-configuração)
- [Rodando o projeto](#rodando-o-projeto)
- [Rotas da aplicação web](#rotas-da-aplicação-web)
- [API REST](#api-rest)
- [Fluxo de telemetria](#fluxo-de-telemetria)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Administração](#administração)
- [Observações importantes](#observações-importantes)
- [Possíveis evoluções](#possíveis-evoluções)

---

## Sobre o projeto

## 📋 Sobre o RACK+
O **RACK+** é uma solução especializada na gestão de infraestrutura física e lógica de redes. O sistema foi projetado para resolver o problema de visibilidade de ativos em centros de dados e salas de rede, permitindo o controle hierárquico **Salas -> Racks -> Dispositivos** e o monitoramento em tempo real do estado desses equipamentos.

Na prática, o sistema permite:

- cadastrar e organizar salas técnicas
- estruturar racks dentro de cada sala
- manter inventário dos dispositivos instalados
- visualizar o estado operacional dos devices
- registrar e consultar histórico de telemetria
- integrar scripts externos via API REST

---

## Objetivo do sistema

O RACK+ foi desenhado para separar duas responsabilidades que normalmente se misturam:

- **inventário estático**, com localização e especificações dos ativos
- **monitoramento dinâmico**, com status atual e histórico operacional

Por isso, o projeto segue a seguinte divisão:

- `Device` guarda apenas dados estáticos do inventário
- `DeviceTelemetry` representa o estado atual do equipamento
- `TelemetryLog` mantém o histórico completo das coletas

Essa separação evita inconsistências como cadastrar manualmente bateria, status de conexão ou uso de armazenamento no momento da criação do device.

---

## Principais funcionalidades

### Interface web

- dashboard com listagem de salas
- navegação hierárquica entre salas, racks e devices
- busca por salas, racks e devices
- CRUD de salas
- CRUD de racks
- CRUD de devices
- tela de detalhe do device com inventário e telemetria
- histórico recente de telemetria por dispositivo

### API REST

- CRUD completo para `Sala`
- CRUD completo para `Rack`
- CRUD completo para `Device`
- CRUD para `TelemetryLog`
- autenticação por sessão ou Basic Auth
- sincronização automática da telemetria atual a partir de novos logs

---

## Modelagem do domínio

### `Sala`
Representa o espaço físico onde ficam racks e equipamentos.

Campos principais:

- `nome`
- `localizacao`
- `criado_em`

### `Rack`
Representa um rack físico dentro de uma sala.

Campos principais:

- `nome`
- `sala`
- `criado_em`

### `Device`
Representa o inventário estático do equipamento.

Campos principais:

- `serial_id`
- `rack`
- `processador`
- `ram`
- `armazenamento_total_gb`
- `criado_em`

### `DeviceTelemetry`
Representa a telemetria atual do dispositivo.

Campos principais:

- `device`
- `bateria_pct`
- `status_conexao`
- `armazenamento_usado_gb`
- `ultimo_log`
- `atualizado_em`

### `TelemetryLog`
Representa o histórico de telemetria do dispositivo.

Campos principais:

- `device`
- `bateria_pct`
- `status_conexao`
- `armazenamento_usado_gb`
- `registrado_em`

### Status de conexão suportados

- `conectado_carregando`
- `conectado`
- `desconectado`
- `problema`

---

## Tecnologias utilizadas

- Python 3
- Django 6
- Django REST Framework
- MySQL
- Bootstrap 5
- python-decouple

Dependências principais do projeto:

- `Django==6.0.4`
- `djangorestframework==3.17.1`
- `mysqlclient==2.2.8`
- `python-decouple==3.8`

---

## Estrutura do projeto

```text
RACK+ PROJECT/
├── core/                    # Configurações globais do Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── gestao/                  # App principal
│   ├── models.py            # Sala, Rack, Device, TelemetryLog
│   ├── views.py             # Views web com @login_required
│   ├── api_views.py         # ViewSets da API REST
│   ├── serializers.py       # ModelSerializers do DRF
│   ├── forms.py             # Formulários de criação e edição
│   ├── urls.py              # Rotas web e API
│   └── admin.py             # Configuração do painel admin
│   └── migrations/
├── static/                  # CSS e imagens
├── templates/               # Templates HTML
├── .env                      # Variáveis de ambiente (não versionado)
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## Pré-requisitos

- Python 3.12 ou superior
- MySQL 8 ou superior
- Git

> O projeto está configurado para usar MySQL como banco principal.

---

## Instalação e configuração

### 1. Clone o repositório

```bash
git clone https://github.com/CaioGomes26/django-rackplus-project.git
cd django-rackplus-project
```

### 2. Crie e ative o ambiente virtual

No Windows CMD:

```bash
python -m venv venv
venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Crie o banco de dados

Exemplo de criação no MySQL:

```sql
CREATE DATABASE rackplus CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True

DB_NAME=rackplus
DB_USER=seu_usuario_mysql
DB_PASSWORD=sua_senha_mysql
DB_HOST=localhost
DB_PORT=3306
```

> O arquivo `.env` não deve ser versionado. Ele já está ignorado no `.gitignore`.

### 6. Aplique as migrações

```bash
python manage.py migrate
```

### 7. Crie um superusuário

```bash
python manage.py createsuperuser
```

---

## Rodando o projeto

```bash
python manage.py runserver
```

A aplicação ficará disponível em:

- [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Painel administrativo:

- [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Rotas da aplicação web

Todas as rotas abaixo exigem autenticação, com exceção do login.

### Autenticação

| Rota | Método | Descrição |
|------|--------|-----------|
| `/login/` | `GET`, `POST` | Página de login e autenticação |
| `/logout/` | `POST` | Encerrar sessão |

### Navegação principal

| Rota | Método | Descrição |
|------|--------|-----------|
| `/` | `GET` | Dashboard inicial com listagem de salas |
| `/salas/<id>/` | `GET` | Detalhe da sala com seus racks |
| `/racks/<id>/` | `GET` | Detalhe do rack com seus devices |
| `/devices/<id>/` | `GET` | Detalhe do device com inventário e telemetria |

### CRUD de salas

| Rota | Método | Descrição |
|------|--------|-----------|
| `/sala/nova/` | `GET`, `POST` | Criar nova sala |
| `/sala/<id>/editar/` | `GET`, `POST` | Editar sala |
| `/sala/<id>/deletar/` | `GET`, `POST` | Excluir sala |

### CRUD de racks

| Rota | Método | Descrição |
|------|--------|-----------|
| `/rack/novo/` | `GET`, `POST` | Criar novo rack |
| `/rack/<id>/editar/` | `GET`, `POST` | Editar rack |
| `/rack/<id>/deletar/` | `GET`, `POST` | Excluir rack |

### CRUD de devices

| Rota | Método | Descrição |
|------|--------|-----------|
| `/devices/novo/` | `GET`, `POST` | Criar novo device |
| `/devices/<id>/editar/` | `GET`, `POST` | Editar device |
| `/devices/<id>/excluir/` | `GET`, `POST` | Excluir device |

---

## API REST

Base URL:

- `/api/`

Todos os endpoints da API exigem autenticação.

### Métodos de autenticação

- `BasicAuthentication`
- `SessionAuthentication`

### Endpoints disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/salas/` | Lista todas as salas |
| `POST` | `/api/salas/` | Cria uma sala |
| `GET` | `/api/salas/<id>/` | Detalhe de uma sala |
| `PUT/PATCH` | `/api/salas/<id>/` | Atualiza uma sala |
| `DELETE` | `/api/salas/<id>/` | Remove uma sala |
| `GET` | `/api/racks/` | Lista todos os racks |
| `POST` | `/api/racks/` | Cria um rack |
| `GET` | `/api/racks/<id>/` | Detalhe de um rack |
| `PUT/PATCH` | `/api/racks/<id>/` | Atualiza um rack |
| `DELETE` | `/api/racks/<id>/` | Remove um rack |
| `GET` | `/api/devices/` | Lista todos os devices |
| `POST` | `/api/devices/` | Cria um device |
| `GET` | `/api/devices/<id>/` | Detalhe de um device |
| `PUT/PATCH` | `/api/devices/<id>/` | Atualiza um device |
| `DELETE` | `/api/devices/<id>/` | Remove um device |
| `GET` | `/api/logs/` | Lista logs de telemetria |
| `POST` | `/api/logs/` | Registra novo log de telemetria |
| `GET` | `/api/logs/<id>/` | Detalhe de um log |
| `PUT/PATCH` | `/api/logs/<id>/` | Atualiza um log |
| `DELETE` | `/api/logs/<id>/` | Remove um log |

### Exemplo de criação de log de telemetria

```bash
curl -X POST http://127.0.0.1:8000/api/logs/ \
  -u usuario:senha \
  -H "Content-Type: application/json" \
  -d '{
    "device": 1,
    "bateria_pct": 87,
    "status_conexao": "conectado_carregando",
    "armazenamento_usado_gb": 210
  }'
```

### Status codes mais comuns

| Código | Situação |
|--------|----------|
| `200` | Requisição bem-sucedida |
| `201` | Recurso criado com sucesso |
| `400` | Dados inválidos |
| `401` | Não autenticado |
| `404` | Recurso não encontrado |
| `405` | Método não permitido |

---

## Fluxo de telemetria

O fluxo esperado de monitoramento é:

1. o device já existe no inventário
2. um script externo coleta informações operacionais
3. esse script envia um novo registro para `/api/logs/`
4. o sistema salva o histórico em `TelemetryLog`
5. o sistema atualiza ou cria o estado atual em `DeviceTelemetry`
6. a interface web passa a exibir o status atualizado do equipamento

### Resumo da responsabilidade de cada camada

- `Device`: inventário manual
- `TelemetryLog`: histórico de eventos
- `DeviceTelemetry`: snapshot atual usado pela interface

---

## Variáveis de ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `SECRET_KEY` | Chave secreta do Django | — |
| `DEBUG` | Modo de depuração | `False` |
| `DB_NAME` | Nome do banco de dados | — |
| `DB_USER` | Usuário do MySQL | — |
| `DB_PASSWORD` | Senha do MySQL | — |
| `DB_HOST` | Host do MySQL | `localhost` |
| `DB_PORT` | Porta do MySQL | `3306` |

---

## Administração

O Django Admin está disponível em:

- `/admin/`

No painel administrativo, o projeto permite gerenciar:

- salas
- racks
- devices
- telemetria atual
- logs de telemetria

---

## Observações importantes

- o projeto usa MySQL como banco principal
- a API exige autenticação para todos os endpoints
- os campos de telemetria não fazem parte do cadastro manual do device
- a telemetria atual é derivada dos logs recebidos por automação
- a estrutura da API está propositalmente plana, sem aninhamento automático de salas, racks e devices

---

## Possíveis evoluções

- dashboard consolidado de monitoramento
- alertas por falha, bateria crítica ou desconexão
- filtros avançados por sala, rack e estado do device
- paginação e documentação formal da API
- integração com agentes de coleta em tempo real
- controle de permissões por perfil de usuário
- exportação de inventário e relatórios

---

## Autor
- Caio Gomes de Oliveira