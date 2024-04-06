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
sudo -i -u postgres psql < scripts/createdb.sql
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
3. git merge __seu nome__
4. git push

### Pulling
Ao realizar um git pull, se houve modificações se torna necessário atualizar a branch com seu nome também. Para isso siga os seguintes passos:

1. git switch __seu nome__
2. git merge main

Caso houver conflito me procure(João).

## Django admin
**IMPORTANTE:** Use o comando `python manage.py createsuperuser` para criar um usuário administrador com as credendicias abaixo.

Credenciais para acessar o "/admin" são as seguintes:
- usuário: adm_adopet
- senha: django8


## json

json modelo para criar um adotante:

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

json modelo para atualizar um adotante: (pode receber informações em partes desde que siga o modelo json abaixo)

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


json modelo para criar usuario:

{
"firstname": "krillin",
"lastname": "catolico",
"email": "krillin@catolico.com",
"password": "senhagrande"
}

