# Izamaravilha Panificadora

## Sumário

- [Izamaravilha Panificadora](#izamaravilha-panificadora)
  - [Sumário](#sumário)
  - [1. Resumo](#1-resumo)
    - [1.1. Time](#11-time)
  - [2. Diagrama de entidades e relacionamentos](#2-diagrama-de-entidades-e-relacionamentos)
  - [3. Preparativos](#3-preparativos)
    - [3.1. Instalando Dependências](#31-instalando-dependências)
    - [3.2. Variáveis de ambiente](#32-variáveis-de-ambiente)
    - [3.3. Entrando no ambiente virtual](#33-entrando-no-ambiente-virtual)
    - [3.4. Instale as dependências](#34-instale-as-dependências)
    - [3.4. Execute as migrações para realizar a persistência de dados](#34-execute-as-migrações-para-realizar-a-persistência-de-dados)
  - [4. Autenticação](#4-autenticação)

---

## 1. Resumo

Essa API foi estruturada no intuito de facilitar a manipulação de dados do back-end do nosso projeto.

Izamaravilha Panificadora é uma plataforma focada em resolver o problema de uma solicitação de uma empresa
na qual necessita de um sistema de gerenciamento, essa API foi baseada em CRUD (Create-Read-Update-Delete):

- **Usuários**
- **Produtos**
- **Estoque**

Quanto as outras rotas e entidades utilizadas, devido à possibilidade de utilização de dados e relações,
essas são as nossas três principais entidades.

Tecnologias usadas nesse projeto:

- [DJango](https://www.djangoproject.com/)
- [DJango Rest Framework](https://www.django-rest-framework.org/)
- [Psycopg2-binary](https://pypi.org/project/psycopg2-binary/)
- [Black](https://pypi.org/project/black/)
- [Gunicorn](https://gunicorn.org/)
- [Coverage](https://pypi.org/project/coverage/)
- [IPython](https://pypi.org/project/ipython/)
- [IPDB](https://pypi.org/project/ipdb/)

**Base URL: https://izamaravilha-project.herokuapp.com/api/swagger/**

### 1.1. Time

> - [Erick Guimarães Marchetti](https://github.com/erickmarchetti) - TL
> - [Hítalo Santos da Silva](https://github.com/hitaloss) - PO
> - [Bruno Tibério Santinoni de Oliveira](https://github.com/brunotiberio) - SM
> - [Fidel Marques Netto](https://github.com/fidelmarques) - Dev
> - [Andryws Görtz Ferreira Rodrigues Seixas](https://github.com/AndrywsKenzie) - Dev
> - [Izamara Agata Rodrigues Machado](https://github.com/izamaraa) - Dev

---

## 2. Diagrama de entidades e relacionamentos

[ Voltar ao topo ](#sumário)

![ERD](<[/diagram-er.png](https://drive.google.com/file/d/1E7HWnj8lBfhXLGLWDmS0lR7gwxZYrFDR/view)>)

---

## 3. Preparativos

[ Voltar ao topo ](#sumário)

### 3.1. Instalando Dependências

Clone o projeto em sua máquina local e instale o ambiente virtual VENV:

```shell
python -m venv venv
```

### 3.2. Variáveis de ambiente

Crie um arquivo **.env** no diretório raiz do projeto, copiando o exemplo do **.env.example**:

```shell
cp .env.example .env
```

Atribua suas variáveis de ambiente às credenciais do seu PostgreSQL à um database da sua escolha.

### 3.3. Entrando no ambiente virtual

Entre no ambiente virtual com o comando:

**Windows**

```shell
source venv/Scripts/activate                    # terminal BASH
```

ou

```shell
.\venv\Scripts\activate                         # terminal powershell
```

**Linux**

```shell
source venv/bin/activate
```

### 3.4. Instale as dependências

Dependências necessárias para rodar o projeto:

```shell
pip install -r requirements.txt
```

### 3.4. Execute as migrações para realizar a persistência de dados

**Windows**

```shell
.\manage.py migrate                 # terminal BASH
```

ou

```shell
python manage.py migrate            # terminal powershell
```

**Linux**

```shell
./manage.py migrate
```

---

## 4. Autenticação

[ Voltar ao topo ](#sumário)

Algumas rotas necessitam de autenticação, utilizando o tipo **Token**.
