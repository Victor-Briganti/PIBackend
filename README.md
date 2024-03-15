# Manus ONG (Projeto Integrador)

## Sobre

Esta aplicação foi criada para simplificar a adoção de animais de estimação. Oferecendo uma plataforma intuitica que permite aos usuários visualizar perfis detalhados dos animais disponíveis.

Ao utilizar a aplicação, os usuários podem filtrar os animais de acordo com suas preferências, facilitando a busca pelo companheiro perfeito. A plataforma também garante um processo de adoção transparente e responsável, desde o cadastro inicial até o acompanhamento pós-adotivo.

## Instalação

```bash

# Inicialize o ambiente virtual
virtualenv .venv
source .venv/bin/activate

# Instalação dos pacotes importantes
pip install django

# Instalação do linter
pip install pylint-django
```

### Banco de dados

**Instalação:**

```bash
# Instala postgresql
sudo apt install postgresql postgresql-contrib

# Instala o adaptador para o banco
pip install psycopg
```

**Configuração:**
```bash 
sudo -i -u postgres psql
```

```SQL
-- Cria o banco de dados
CREATE DATABASE manusbd;

-- Cria o usuário
CREATE USER adm_manus WITH PASSWORD 'django8';

-- Configurações necessárias para o funcionamento do django
ALTER ROLE adm_manus SET client_encoding TO 'utf8';
ALTER ROLE adm_manus SET default_transaction_isolation TO 'read committed';
ALTER ROLE adm_manus SET timezone TO 'UTC';

-- Dá privilégios aos usuários
GRANT ALL PRIVILEGES ON DATABASE manusbd TO adm_manus;

-- Versão 15 do postgresql
-- Permite que o banco de dados seja alterado pelo administrador
ALTER DATABASE manusbd OWNER TO adm_manus;
```

## Contribuindo

### Mensagens de Commit

Por padrão as mensagens de commit devem seguir o seguinte padrão:

[Nome da funcionalidade] Titulo da modificação

Breve descrição(Não passar de 3 linhas).

### Commit
Utilize uma branch com o seu nome para realizar as modificações no programa. **NÃO** suba essa branch para o github, ela deve ser de uso local.

**PASSOS:**
1. Mudar para a branch main
2. git pull
3. mudar para a branch com seu nome
4. git merge <seu nome>
5. git push

### Pulling
Ao realizar um git pull, se houve modificações se torna necessário atualizar a branch com seu nome também. Para isso siga os seguintes passos:

1. git switch <seu nome>
2. git merge main

Caso houver conflito me procure(João).

## Django admin
**IMPORTANTE:** Use o comando `python manage.py createsuperuser` para criar um usuário administrador com as credendicias abaixo.

Credenciais para acessar o "/admin" são as seguintes:
- usuário: adm_manus
- senha: django8
