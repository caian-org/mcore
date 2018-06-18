# MakeYourFrete: Core API

O projeto da API foi desenvolvido com o sistema **GNU/Debian 9**. As instruções
a seguir foram descritas levando este sistema em consideração. Distribuições
GNU/Linux baseadas em Debian como o **Ubuntu** ou **Linux Mint** são
candidatos, embora alguns comandos possam diferir.

Os comandos partem da premissa que o usuário possui permissões de superusuário.
Caso o usuário não possua permissão para escrever no sistema, utilize `sudo` ou
altere para outro que possua as permissões necessárias.

## Índice

- [Instalação dos requerimentos](#instalação-dos-requerimentos)
  - [Instalando o Python 3.5](#instalando-o-python-35)
  - [Instalando o pip3](#instalando-o-pip3)
  - [Instalando o pipenv](#instalando-o-pipenv)
  - [Instalando o SQLite](#instalando-o-sqlite)
- [Instalação das dependências](#instalação-das-dependências)
- [Execução do servidor](#execução-do-servidor)
- [Execução dos testes](#execução-dos-testes)
- [Documentação da API](#documentação-da-api)


## Instalação dos requerimentos

Os seguintes softwares são necessários para a execução do projeto:

- [Python 3.5](https://www.python.org/downloads/release/python-350/)
- [pip3](https://pip.pypa.io/en/stable/)
- [pipenv](https://docs.pipenv.org/)
- [SQLite](https://www.sqlite.org/)

### Instalando o Python 3.5

```sh
$ apt-get install python3
```

### Instalando o pip3

```sh
$ apt-get install python3-pip
```

### Instalando o pipenv

```sh
$ pip3 install pipenv
```

### Instalando o SQLite

```sh
$ apt-get install sqlite3 libsqlite3-dev
```


## Instalação das dependências

- **Acesse o repositório do projeto**

```sh
$ cd /caminho/do/repositorio
```

- **Crie o ambiente virtual & instale as dependências**

```sh
$ pipenv install
```

- **Instale as dependências de desenvolvimento**

```sh
$ pipenv install --dev
```

*PS: As dependências de desenvolvimento são necessárias para a execução dos
testes.*


## Execução do servidor

Já dentro do repositório do projeto...

- **Invoque o ambiente virtual**

```sh
$ make env
```

- **Execute o servidor**

```sh
$ make run
```

*PS: O servidor estará escutando as requisições na porta 8080.*

## Execução dos testes

Já dentro do repositório do projeto, tendo invocado o ambiente virtual...

- **Execute os testes**

```sh
$ make test
```

Cada teste é executado contra um dos recursos REST da API, de modo automático.
Ao final da execução dos testes, o banco estará populado com informações
aleatórias geradas em tempo de execução.


## Documentação da API

A documentação de uso dos recursos e rotas da API estão disponíveis
[aqui](https://caianrais.github.io/mcore-docs/).
