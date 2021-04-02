# BetBot

![BetBot Video](.github/video.gif)


> Um automatizador de apostas para a plataforma Bet365. O objetivo foi de criar uma interface responsiva, mas que se comunique com o script python. 

## Tecnologias usadas
- Selenium para controle na Bet365.
- Eel para construção da interface
- MongoDB para armazenamento de usuários

## Dificuldades
A catalogação de cada tipo de botão além do acesso a plataforma de forma a não ser visto como bot. Além da preocupação estética para se parecer com a plataforma, sem esquecer dos efeitos visuais e interações, de forma a manter um padrão de qualidade para o usuário. No meio do projeto foi necessário trocar do Google Chrome para o Firefox pois foi bloqueado o acesso a partir do Chrome.

## Como utilizar
1. Instale o python 3.9, e na raiz do projeto instale as [dependências]((./requirements.txt)):
```bash
pip install -r requirements.txt
```
2. Certifique-se que tem uma conta na [Bet 365](https://www.bet365.com/), e pegue o seu nome de usuário e senha.
3. Certifique-se que tem o [Firefox](./widgets.py) instalado com o seu respectivo Gecko Driver 
4. Crie uma conta no [MongoDB](https://medium.com/reprogramabr/conectando-no-banco-de-dados-cloud-mongodb-atlas-bca63399693f#:~:text=Acesse%20ao%20site%20do%20MongoDB,esquerdo%2C%20clique%20em%20Database%20Access.), um Cluster para criar uma Database chamada [betbot](./database.py) com uma Collection chamada users
5. Crie um arquivo na raiz do projeto chamado env.py com a [autenticação](https://docs.atlas.mongodb.com/tutorial/connect-to-your-cluster/) do seu Mongo:
```py
autenticacao = "mongodb+srv://<USUARIOMONGO>:<SENHAMONHO>@cluster<CLUSTERID>.mongodb.net/betbot?retryWrites=true&w=majority"
```
6. Adicione a seguinte linha no final do database.py na primeira vez:
```py
MongoDB.cadastrar("NOMEDOUSUARIO", "SENHA") # Nome do usuário da conta da Bet e sua senha
```
7. Inicie o [interface.py](./interface.py) e faça o login, e então retire a linha adicionada anteriormente.

![Config Video](.github/configVideo.gif)
