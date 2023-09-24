# Auth Service
Projeto criado como componente C do MVP da disciplina de Back-end avançado do curso de pós-graduação em Desenvolvimento Full Stack da PUC-Rio.

## O que é?
Serviço para criação, edição, autenticação e autorização de usuários utilizado na aplicação ([Got that ref](https://github.com/amandagpearce/got-that-ref))

### Rodando o projeto com Docker
1. Clone o projeto
2. Na raiz do projeto, crie a imagem:
```bash
  docker build -t auth-service .
```

3. Rode a imagem criada:
```bash
  docker run -p 5000:5000 auth-service
```

