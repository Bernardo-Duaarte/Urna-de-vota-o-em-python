# 🗳️ Urna Eletrônica - API Flask + PostgreSQL

Este projeto é uma simulação de uma **urna eletrônica** construída em **Flask** com integração ao banco de dados **PostgreSQL**.  
Ele permite cadastrar candidatos, registrar votos e consultar resultados em tempo real via API.

---

## 🚀 Tecnologias utilizadas
- Python 3.12+
- Flask
- SQLAlchemy
- PostgreSQL
- HTML (templates simples)

---

## 📂 Estrutura do projeto

Urna/
├── app.py # Configuração principal do Flask

├── config.py # Configurações (inclui banco de dados)

├── models.py # Definição das tabelas do banco

├── routes.py # Rotas da API (votação, resultados, cadastro)

├── run.py # Script para rodar o servidor

├── test_stress.py # Testes de stress da API

├── init_db.py # Script para criar tabelas e candidatos de exemplo

├── init_eleitores.py # Script para criar eleitores de exemplo

├── templates/

│ └── index.html # Página inicial simples

---

## ⚙️ Passo a passo (executar sempre dentro da pasta `Urna/`)

### 🔹 1. Clonar o repositório

git clone https://github.com/SEU_USUARIO/urna-eletronica.git
cd urna-eletronica/Urna

### 🔹 2. Criar e ativar ambiente virtual
Linux / macOS:

bash

python -m venv venv
source venv/bin/activate
Windows (PowerShell):

powershell

python -m venv venv
.\venv\Scripts\Activate.ps1   # ou: .\venv\Scripts\activate

### 🔹 3. Instalar dependências

bash
pip install -r requirements.txt

###🔹 4. Configurar conexão com PostgreSQL

Defina a variável de ambiente DATABASE_URL ou edite config.py.
Exemplo:

Linux / macOS:
bash
export DATABASE_URL="postgresql://usuario:senha@localhost:5432/votacao"

Windows (PowerShell):
powershell
$env:DATABASE_URL = "postgresql://usuario:senha@localhost:5432/votacao"

###🔹 5. Criar banco de dados no PostgreSQL

bash
psql -U postgres -h localhost -W -c "CREATE DATABASE votacao;"

###🔹 6. Inicializar tabelas e candidatos de exemplo

Um script já foi criado (init_db.py). Execute:
bash
python init_db.py
Isso cria as tabelas e adiciona:

Candidato A

Candidato B

Servidor rodará em:
👉 http://localhost:5000

📌 Endpoints principais
###🔹 Listar candidatos
bash
Copiar código
curl http://localhost:5000/candidatos
###🔹 Cadastrar eleitor
bash
Copiar código
curl -X POST http://localhost:5000/cadastrar \
  -H "Content-Type: application/json" \
  -d '{"cpf":"12345678901","nome":"Fulano de Tal"}'
###🔹 Votar
bash
Copiar código
curl -X POST http://localhost:5000/votar \
  -H "Content-Type: application/json" \
  -d '{"cpf":"12345678901","candidato_id":1}'
###🔹 Resultados
bash
Copiar código
curl http://localhost:5000/resultados
Retorno:

json
Copiar código
[
  {"id": 1, "nome": "Candidato A", "votos": 10},
  {"id": 2, "nome": "Candidato B", "votos": 5}
]
###🧪 Testes
Rodar unit tests:

bash
Copiar código
pytest
Rodar stress test:

bash
Copiar código
python test_stress.py
├── test_stress.py # Testes de stress da API

├── templates/

│ └── index.html # Página inicial simples

