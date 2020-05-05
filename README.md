## Laguinho [![chat on Discord](https://img.shields.io/discord/558293573494112257.svg?logo=discord)](https://discordapp.com/invite/vFFGGEE)
  
Interface de linha de comando (CLI) para publicar e recuperar dados no [laguinho-api](https://github.com/OpenDevUFCG/laguinho-api/)

## Desenvolvimento

Este projeto é feito utilizando [Python 3](https://www.python.org/), você precisa tê-lo [instalado](https://www.python.org/downloads/) na sua máquina.

### Configurando a máquina

``` bash
# instalando o pipenv
$ pip install --user pipenv
```

### Configurando o projeto

``` bash
# clonando o repositório
$ git clone https://github.com/OpenDevUFCG/laguinho.git
$ cd laguinho

# instalando as dependências
$ pipenv install

# executando o script de inicialização da versão de desenvolvimento 
$ pipenv run laguinho-dev [COMANDO]
```

### Gerando um Github Token

![github_token](https://user-images.githubusercontent.com/33502846/67691356-33fda580-f97d-11e9-82c2-315ea2dd7358.gif)

#### Passo a passo

Para baixar os dados pelo comando `get`, é necessário fornecer um token de autenticação do Github, para gerá-lo basta seguir os passos descritos abaixo ou acesse este [link](https://github.com/settings/tokens/new) e pule para o passo 5:

1. Primeiramente, acesse a sua [página de configurações do Github](https://github.com/settings/profile)
2. Selecione a aba `Developer Settings`
3. Vá em `Personal Access Token`
4. Clique em `Generate new Token`
5. Adicione um nome e selecione a caixa de escolha `user`
6. Clique em `Generate token`
7. Copie o token gerado (obs: tenha certeza de ter copiado, uma vez que ele não será disponilizado novamente, apenas ao criar um novo token) e cole na CLI quando requisitado ou executando o comando `configure`.

## Como Contribuir

Quer implementar alguma nova funcionalidade ou corrigir algum bug? Pode ir dando uma olhada nas issues abertas pra saber no que estamos trabalhando ou se preferir pode abrir sua própria caso queira corrigir ou adicionar algo novo! 

Qualquer dúvida é só procurar a gente via [discord](https://discord.gg/vMcuNtt) ou pelas issues mesmo!  

OBS: Esse ainda é um projeto em desenvolvimento, para acompanhar melhor, tudo começou com [esta issue no laguinho-api](https://github.com/OpenDevUFCG/laguinho-api/issues/31), a partir dela você consegue chegar em toda a discussão sobre a CLI
