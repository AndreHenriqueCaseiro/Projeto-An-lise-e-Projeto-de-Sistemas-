# Projeto de Análise e Projeto de Sistemas: Gestão de Itens

Este repositório contém o código-fonte do backend para um sistema de gestão de produtos e itens, desenvolvido como parte da disciplina de Análise e Projeto de Sistemas.

A API é construída em Python usando o framework FastAPI e se conecta a um banco de dados PostgreSQL.

## Tecnologias e Ferramentas

* **Linguagem:** Python 3.10+
* **Framework Web (API):** FastAPI
* **Servidor ASGI:** Uvicorn
* **Banco de Dados:** PostgreSQL
* **ORM (Mapeamento Objeto-Relacional):** SQLAlchemy
* **Validação de Dados:** Pydantic
* **Editor de Código:** Visual Studio Code
* **Controle de Versão:** Git & GitHub

---

## Guia de Construção e Configuração do Ambiente

Esta seção detalha o passo a passo da construção da base do projeto, servindo como um guia de instalação e um registro do desenvolvimento inicial.

### **Passo 0: Configuração Inicial do Ambiente**

* **Objetivo:** Preparar o ambiente de desenvolvimento local.
* **Ferramentas:** Terminal (Git Bash), Python.
* **Ações:**
    1.  Criação da pasta do projeto (`gestao_itens`).
    2.  Criação de um ambiente virtual com o comando `python -m venv venv` para isolar as dependências do projeto.
    3.  Ativação do ambiente virtual com `source venv/Scripts/activate`.

### **Passo 1: Instalação das Dependências**

* **Objetivo:** Instalar todas as bibliotecas Python necessárias.
* **Ferramentas:** `pip` (gerenciador de pacotes do Python).
* **Ações:**
    1.  Criação do arquivo `requirements.txt` para listar as dependências.
    2.  Instalação de todas as bibliotecas de uma vez com o comando `pip install -r requirements.txt`.

### **Passo 2: Criação do Banco de Dados e Tabelas**

* **Objetivo:** Configurar a estrutura inicial do banco de dados.
* **Ferramentas:** Visual Studio Code com a extensão **SQLTools** e o driver do PostgreSQL.
* **Ações:**
    1.  Conexão com o servidor PostgreSQL local através do SQLTools.
    2.  Execução do comando `CREATE DATABASE gestao_db;` para criar o banco de dados do projeto.
    3.  Execução do comando `CREATE TABLE Produtos (...)` para criar a primeira tabela do sistema.

### **Passo 3: Estrutura de Pastas do Projeto**

* **Objetivo:** Organizar o código-fonte de forma lógica e escalável.
* **Ferramentas:** Visual Studio Code.
* **Ações:**
    1.  Criação da pasta principal `app/`.
    2.  Criação das subpastas `models/`, `schemas/` e `routers/` para separar as responsabilidades do código.
    3.  Criação dos arquivos `__init__.py` para que o Python reconheça as pastas como pacotes.

### **Passo 4: Configuração da Conexão (Python e Banco de Dados)**

* **Objetivo:** Permitir que a aplicação Python se conecte ao PostgreSQL.
* **Ferramentas:** Python, SQLAlchemy, Dotenv.
* **Ações:**
    1.  Criação do arquivo `.env` para armazenar de forma segura a string de conexão do banco (`DATABASE_URL`).
    2.  Desenvolvimento do arquivo `app/database.py`, que utiliza o **SQLAlchemy** para criar o "motor" de conexão com o banco de dados.

### **Passo 5: Criação do Modelo (ORM)**

* **Objetivo:** Mapear a tabela `Produtos` do SQL para uma classe Python.
* **Ferramentas:** Python, SQLAlchemy.
* **Ações:**
    1.  Desenvolvimento do arquivo `app/models/produto_model.py`.
    2.  Criação da classe `Produto` que herda de `Base` (do SQLAlchemy), traduzindo as colunas da tabela em atributos de classe.

### **Passo 6: Criação dos Esquemas (Validação de Dados)**

* **Objetivo:** Definir o "contrato" de dados para a API (o que ela recebe e envia).
* **Ferramentas:** Python, Pydantic (integrado ao FastAPI).
* **Ações:**
    1.  Desenvolvimento do arquivo `app/schemas/produto_schema.py`.
    2.  Criação das classes `ProdutoBase`, `ProdutoCreate` e `Produto` para validar os dados de entrada e formatar os dados de saída da API.

### **Passo 7: Criação do Roteador (Endpoints da API)**

* **Objetivo:** Criar os endereços (URLs) funcionais da API para `Produtos`.
* **Ferramentas:** Python, FastAPI.
* **Ações:**
    1.  Desenvolvimento do arquivo `app/routers/produtos_router.py`.
    2.  Criação dos endpoints `POST /produtos` (para criar) e `GET /produtos` (para listar), definindo a lógica de negócio para cada operação.

### **Passo 8: Montagem da Aplicação Principal**

* **Objetivo:** Juntar todas as peças e criar o ponto de entrada da aplicação.
* **Ferramentas:** Python, FastAPI.
* **Ações:**
    1.  Desenvolvimento do arquivo `app/main.py`.
    2.  Criação da instância principal do FastAPI.
    3.  Inclusão do roteador de produtos (`produtos_router`) na aplicação principal com o comando `app.include_router(...)`.

### **Passo 9: Execução e Teste da API**

* **Objetivo:** Iniciar o servidor e verificar se os endpoints estão funcionando.
* **Ferramentas:** Uvicorn, Navegador Web.
* **Ações:**
    1.  Execução do comando `uvicorn app.main:app --reload` no terminal para iniciar o servidor.
    2.  Acesso à documentação interativa gerada automaticamente pelo FastAPI em `http://127.0.0.1:8000/docs`.
    3.  Teste das rotas de criação e listagem de produtos diretamente pela interface do navegador.