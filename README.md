# Desafio Técnico: Análise de Dados de Voos Comerciais

O objetivo desse projeto é criar uma aplicação que importa dados de voos a partir de um arquivo CSV, armazena esses dados em um banco de dados SQL e disponibiliza uma API REST para consulta dos dados. Além disso, a aplicação deve possuir uma interface web para visualização dos dados em gráficos e tabelas.

---

## **Tecnologias Utilizadas**

- **Python**: Linguagem principal do projeto.
- **Pandas**: Para manipulação e análise de dados.
- **SQLAlchemy**: Para interação com o banco de dados.
- **Flask**: Para a criação da API e interface web.
- **Docker**: Para conteinerização da aplicação.
- **PostgreSQL**: Banco de dados relacional utilizado.
- **Bootstrap**: Para o frontend da aplicação.
- **Chart.js**: Para a criação de gráficos.
---
## **Funcionalidades**

1. **Carga de Dados**:
   - Importação de dados de voos a partir de um arquivo CSV.
   - Filtragem e limpeza dos dados
   - Armazenamento dos dados em um banco de dados SQL.

2. **Consulta de Dados**:
   - API REST para consulta de voos com filtros por mercado, data e ordenação.
   - Dashboard web para visualização dos dados em gráficos e tabelas.

3. **Autenticação**:
   - Sistema de login e registro de usuários.
   - Proteção de rotas com JWT (JSON Web Tokens).

---
## **Instalação**

### **Pré-requisitos**

- Docker e Docker Compose instalados.

### **Passos para Execução**

1. Clone o repositório:
   ```bash
   git clone https://github.com/matheuss0xf/challenge-gol.git
   cd challenge-gol
    ```
2. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:
    ```bash
   DB_NAME=app_db
   DB_HOST=challenge-db
   DB_PORT=5432
   DB_USER=secret
   DB_PASSWORD=secret
   
   DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
   JWT_SECRET_KEY=secret
   FLASK_SECRET_KEY=secret
    ```
3. Inicie os contêineres com Docker Compose:
    ```bash
   docker-compose up --build
    ```
4. Acesse a aplicação em `http://localhost:5000`.
5. Para encerrar a aplicação, pressione `Ctrl + C` e execute o comando:
    ```bash
   docker-compose down
    ```
---
## **API**

### **Rotas**

- **POST** `/auth/register`: Cria um novo usuário.
  - **Body**:
   ```
   {
     "name": "Nome do Usuário",
     "email": "usuario@example.com",
     "password": "senha123",
   }
   ```
- **POST** `/auth/login`: Autentica um usuário e retorna um token JWT.
  - **Body**:
   ```
   {
     "email": "usuario@example.com",
     "password": "senha123",
   }
    ```
- **GET** `/api/flights`: Consulta de voos com filtros e ordenação.
 - **headers**:
    - `Authorization`: Token JWT.
  - Parâmetros:
    - `market`: Filtra por mercado (ex: SBGRSBSP).
    - `date`: Filtra por intervalo de datas (ex: 2023/01;2023/06).
    - `sort`: Ordenação (ex: year:asc,month:asc).

### **Exemplo de uso**
![api](https://github.com/user-attachments/assets/5b6b6723-263b-42b7-a2c9-bb63e48c453a)
