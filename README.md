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
```
#posgree instalation and config

#script para conf do postgres
 #instala postgres
sudo apt install postgresql postgresql-contrib

#depois de instalar

sudo -i -u postgres

psql

#criando database (dentro do psql)

create database manusbd;
#criando user

create user adm_manus with password 'django8';
alter role adm_manus set client_encoding to 'utf8'; 
alter role adm_manus set default_transaction_isolation to 'read committed'; 
alter role adm_manus set timezone to 'UTC';

GRANT all privileges on database manusbd to adm_manus;


