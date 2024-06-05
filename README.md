# Adopet ONG (Projeto Integrador)

## Tecnologias

<p align="center">
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"/>
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
</p>

## Participantes

- João Victor Briganti de Oliveira
- Pedro Conrado Negreiro da Silva
- Augusto Maccagnan Mendes
- Matheus Floriano Saito da Silva

## Sobre

Esta aplicação foi criada para simplificar a adoção de animais de estimação. Oferecendo uma plataforma intuitica que permite aos usuários visualizar perfis detalhados dos animais disponíveis.

Ao utilizar a aplicação, os usuários podem filtrar os animais de acordo com suas preferências, facilitando a busca pelo companheiro perfeito. A plataforma também garante um processo de adoção transparente e responsável.

## Instalação

```bash

# Inicialize o ambiente virtual
virtualenv .venv
source .venv/bin/activate

# Instalação dos pacotes importantes
pip install -r requirements.txt
```

### Banco de dados

**Instalação:**

```bash
# Instala postgresql
sudo apt install postgresql postgresql-contrib
```

**Configuração:**

```bash
# DELETA o banco de dados
sudo -i -u postgres psql < scripts/deletedb.sql

# Cria o banco de dados
sudo -i -u postgres psql < scripts/createdb.sql

#############################################################
#### MIGRATE PRECISA SER FEITO ANTES DOS COMANDOS ABAIXO ####
#############################################################

### A ORDEM ABAIXO PRECISA SER RESPEITADA ###

# Adiciona os estados ao banco de dados
sudo -i -u postgres psql adopetbd < scripts/state.sql

# Adiciona as cidades ao banco de dados
sudo -i -u postgres psql adopetbd < scripts/city.sql

# Adiciona as endereços ao banco de dados
sudo -i -u postgres psql adopetbd < scripts/address.sql

# Adiciona os usuários ao banco de dados
sudo -i -u postgres psql adopetbd < scripts/user.sql

# Adiciona os metadados de usuário ao banco de dados
sudo -i -u postgres psql adopetbd < scripts/user_metadata.sql

# Adiciona os animais ao banco de dados
sudo -i -u postgres psql adopetbd < scripts/animal.sql

# Adiciona os imagens dos animais ao banco de dados
sudo -i -u postgres psql adopetbd < scripts/animalimage.sql
```

## Contribuindo

### Migrate

O django faz boa parte da administração do banco de dados, por esse motivo sempre antes de dar um novo commit, certifique-se de executar os seguintes passos:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Mensagens de Commit

Por padrão as mensagens de commit devem seguir o seguinte padrão:

[Nome da funcionalidade] Titulo da modificação

Breve descrição(Não passar de 3 linhas).

### Commit

Utilize uma branch com o seu nome para realizar as modificações no programa. **NÃO** suba essa branch para o github, ela deve ser de uso local.

**PASSOS:**

1. git switch main
2. git pull
3. git merge **seu nome**
4. git push

### Pulling

Ao realizar um git pull, se houve modificações se torna necessário atualizar a branch com seu nome também. Para isso siga os seguintes passos:

1. git switch **seu nome**
2. git merge main

Caso houver conflito me procure(João).

## Django admin

**IMPORTANTE:** Use o comando `python manage.py createsuperuser` para criar um usuário administrador com as credendicias abaixo.

Credenciais para acessar o "/admin" são as seguintes:

- usuário: adm_adopet
- senha: django8

## Modelos JSON

### Animal

```json
{
  "name": "Ze",
  "age": "adult",
  "specie": "dog",
  "gender": "M",
  "size": "small",
  "coat": "short",
  "weight": 15.0,
  "adoption_date": null,
  "description": "Grande Ze",
  "is_house_trained": true,
  "is_special_needs": false,
  "is_castrated": "false",
  "is_vaccinated":"true",
  "is_adopted": "false"
  
}
```

### Adotante

```json
{
  "adopter": {
    "birth_date": "1988-09-02",
    "phone": "14991679851",
    "cpf": "77777777777",
    "address": {
      "street": "lampkin lane",
      "city": "south pasadena",
      "state": "AL",
      "zip_code": "18639750",
      "number": "1245",
      "district": "haddonfield"
    }
  }
}
```

**Modelo para atualização:**
OBS.: Pode receber informações em partes desde que siga o modelo json abaixo

```json
{
  "cpf": "33333333333",
  "phone": "987654323",
  "birth_date": "1991-06-13",
  "address": {
    "zip_code": "222224",
    "street": "New boston",
    "number": "19",
    "complement": "",
    "city": "New city",
    "state": "RJ",
    "district": "New center"
  }
}
```

### Usuário

Campos como `last_login`, `is_active` e `is_staff` não devem ser preenchidos. Estes campos devem ser atualizados pela própria implementação do Django.

```json
{
  "id": 5,
  "adopter": null,
  "last_login": "2024-04-07T01:43:09.474485Z",
  "is_superuser": true,
  "email": "admin@gmail.com",
  "firstname": "Admin",
  "lastname": "Teste",
  "is_active": true,
  "is_staff": true,
  "groups": [],
  "user_permissions": []
}
```

**Modelo de Criação/Atualização:**

```json
{
  "firstname": "krillin",
  "lastname": "catolico",
  "email": "krillin@catolico.com",
  "password": "senhagrande"
}
```

### Animal

Nem todos os campos são necessários durante a criação do animal. São eles:

- `id` (Este não deve ser passado em hipotese alguma)
- `temperament`
- `adoption_date`
- `is_house_trained`
- `is_special_needs`
- `is_adopted`

OBS.: Pode receber informações em partes desde que siga o modelo json abaixo

```json
{
  "name": "Ze",
  "age": "adult",
  "specie": "dog",
  "gender": "M",
  "size": "small",
  "coat": "short",
  "weight": 15.0,
  "adoption_date": null,
  "description": "Grande Ze",
  "is_house_trained": true,
  "is_special_needs": false,
  "is_castrated": "false",
  "is_vaccinated":"true",
  "is_adopted": "false"
  
}
```
