# Auth Service
Projeto criado como componente C do MVP da disciplina de Back-end avançado do curso de pós-graduação em Desenvolvimento Full Stack da PUC-Rio.

## O que é?
Serviço para criação, edição, autenticação e autorização de usuários utilizado na aplicação ([Got that ref](https://github.com/amandagpearce/got-that-ref))

## Arquivo .env 
Crie um arquivo `.env` que contenha a `JWT_SECRET_KEY` que será usada para autenticar os usuários.

```bash
JWT_SECRET_KEY=suakey
```
Substitua `suakey` pela sua string, ela pode ser gerada por um pacote terceiro (mais seguro) ou ser uma string qualquer da sua escolha (menos seguro). 

### Instalação com Docker
1. Clone o projeto
2. Na raiz do projeto, cole o arquivo `.env` preenchido como descrito na seção anterior
3. Na raiz do projeto, rode o seguinte comando para criar a imagem:
```bash
  docker build -t auth-service .
```
4. Rode a imagem criada:
```bash
  docker run -p 5000:5000 auth-service
```
5. A documentação no Swagger estará disponível em `http://localhost:5000/doc`

### Instalação sem Docker
1. Clone o projeto
2. Na raiz do projeto, cole o arquivo `.env` preenchido como descrito na seção anterior
3. Crie e ative um ambiente virtual
4. Na raiz do projeto, faça a instalação das dependências com o comando:
```bash
  pip install requirements.txt
```
5. Na raiz do projeto, rode o seguinte comando para iniciar o serviço na porta 5000:
```bash
  flask run
```
6. A documentação no Swagger estará disponível em `http://localhost:5000/doc`

## Banco de dados
A aplicação gerencia um banco de dados sqlite com as seguintes tabelas:

### User table
Dados de usuários regulares.

| Field Name | Data Type | Description          |
|------------|-----------|----------------------|
| id         | Integer   | Primary Key          |
| username   | String(80)| Nome de Usuário      |
| password   | String    | Senha                |


### AdminUser table
Dados de usuários administradores.

| Field Name | Data Type | Description          |
|------------|-----------|----------------------|
| id         | Integer   | Primary Key          |
| username   | String(80)| Nome de Usuário      |
| password   | String    | Senha                |


### Token Blocklist table
Armazena tokens que serão considerados inválidos a partir da execução de Logout.

| Field Name | Data Type | Description          |
|------------|-----------|----------------------|
| id         | Integer   | Primary Key          |
| token      | String    |                      |



