# 🗳️ Urna Eletrônica - API Flask + PostgreSQL

Este projeto é uma simulação de uma **urna eletrônica** construída em **Flask** com integração ao banco de dados **PostgreSQL**.  
Ele permite cadastrar eleitores, registrar votos e consultar resultados em tempo real via API.

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

├── routes.py # Rotas da API (votação, resultados)

├── run.py # Script para rodar o servidor

├── test_stress.py # Testes de stress da API

├── templates/
│ └── index.html # Página inicial simples

