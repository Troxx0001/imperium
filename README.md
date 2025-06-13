# Imperium Tech

## Descrição do Projeto
Imperium Tech é um projeto de estudo que demonstra uma plataforma de e-commerce construída com Flask. Possui autenticação de usuários, gerenciamento de produtos e acompanhamento de pedidos, utilizando um banco de dados PostgreSQL via SQLAlchemy.

## Status
Esta aplicação está em desenvolvimento ativo e serve como plataforma de aprendizado. Contribuições e sugestões são bem-vindas.

## Principais Tecnologias
- Python 3
- Flask
- Flask-Login
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Mail
- PostgreSQL

## Ferramentas de Desenvolvimento
- Virtualenv / `venv`
- `pip` para gerenciamento de dependências
- Git para controle de versão

## Como Começar

### Crie e Ative um Ambiente Virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### Instale as Dependências
```bash
pip install -r requirements.txt
```

### Configuração do Banco de Dados
1. Instale o PostgreSQL e crie um banco de dados (ex: `imperium_utf8`).
2. Atualize a URI de conexão em `config.py` se necessário:
   ```python
   SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:senha@localhost:5432/imperium_utf8'
   ```

### Inicialize o Banco de Dados
Execute o script auxiliar para criar todas as tabelas:
```bash
python init_db.py
```

### Execute a Aplicação
```bash
flask --app app run
```
O servidor será iniciado em `http://127.0.0.1:5000` por padrão.

### Scripts de Gerenciamento Inclusos
- `init_db.py` – cria todas as tabelas do banco de dados.
- `criar_admin.py` – cadastra um usuário administrador com senha criptografada.
- `criar_produtos.py` – insere produtos de exemplo.
- `limpar_banco.py` – remove dados mantendo contas de administrador.

## Medidas de Segurança
- As senhas são armazenadas utilizando as funções de hash do Werkzeug.
- A confirmação de conta é feita via tokens de e-mail gerados pelo `itsdangerous`.