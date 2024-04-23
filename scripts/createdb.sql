-- Cria o banco de dados
CREATE DATABASE adopetbd;

-- Cria o usuário
CREATE USER adm_adopet WITH PASSWORD 'django8';

-- Configurações necessárias para o funcionamento do django
ALTER ROLE adm_adopet 
SET 
  client_encoding TO 'utf8';
ALTER ROLE adm_adopet 
SET 
  default_transaction_isolation TO 'read committed';
ALTER ROLE adm_adopet 
SET 
  timezone TO 'UTC';

-- Dá privilégios aos usuários
GRANT ALL PRIVILEGES ON DATABASE adopetbd TO adm_adopet;

-- Versão 15 do postgresql
-- Permite que o banco de dados seja alterado pelo administrador
ALTER DATABASE adopetbd OWNER TO adm_adopet;
