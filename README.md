# BetBot

![BetBot Video](./docs/images/video.gif)


> Um automatizador de apostas para a plataforma Bet365. O objetivo foi de criar uma interface responsiva, mas que se comunique com o script python. Funciona até o Firefox 85.0.2 ([#10](https://github.com/JDaniloC/Individual-Bet365Bot/issues/10)) e as versões atuais do Chrome.

<div align="center">
	<h2> Idiomas | Languages </h2>
	<a href="https://jdaniloc.github.io/Individual-Bet365Bot/pt/">
		<img src="docs/images/br.png "
		alt="Português" width="50" height="50" />
	</a>
	<a href="https://jdaniloc.github.io/Individual-Bet365Bot/en/">
		<img src="docs/images/en.png "
		alt="English" width="50" height="50"/>
	</a>
</div><br><br>

## Tecnologias usadas
- Selenium para controle na Bet365.
- Eel para construção da interface
- MongoDB para armazenamento de usuários

## Dificuldades
A catalogação de cada tipo de botão além do acesso a plataforma de forma a não ser visto como bot. Além da preocupação estética para se parecer com a plataforma, sem esquecer dos efeitos visuais e interações, de forma a manter um padrão de qualidade para o usuário. No meio do projeto foi necessário trocar do Google Chrome para o Firefox pois foi bloqueado o acesso a partir do Chrome. Mas no fim o Chrome foi novamente possível através do projeto [undected_chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver).

## Como utilizar
1. Instale o python 3.9, e na raiz do projeto instale as [dependências](./requirements.txt):
```bash
pip install -r requirements.txt
```
2. Certifique-se que tem uma conta na [Bet 365](https://www.bet365.com/), e pegue o seu nome de usuário e senha.
3. Certifique-se que tem o [Firefox](./src/widgets.py) instalado com o seu respectivo [Gecko Driver](https://www.take.net/blog/wp-content/cache/wp-rocket/take.net/blog/take-test/instalacao-geckodriver-driver-para-abrir-o-firefox-no-selenium/index-https.html_gzip) no caso de usar o FirefoxBrowser, ou use o ChromeBrowser no [bot.py](./src/bot.py) com o chromedriver.
4. Crie uma conta no [MongoDB](https://medium.com/reprogramabr/conectando-no-banco-de-dados-cloud-mongodb-atlas-bca63399693f#:~:text=Acesse%20ao%20site%20do%20MongoDB,esquerdo%2C%20clique%20em%20Database%20Access.), um Cluster para criar uma Database chamada [betbot](./src/database.py) com uma Collection chamada users.
5. Crie um arquivo na raiz do projeto chamado env.py com a [autenticação](https://docs.atlas.mongodb.com/tutorial/connect-to-your-cluster/) do seu Mongo, sem os <> ([#12](https://github.com/JDaniloC/Individual-Bet365Bot/issues/12)):
```py
autenticacao = "mongodb+srv://<USUARIOMONGO>:<SENHAMONGO>@cluster<CLUSTERID>.mongodb.net/betbot?retryWrites=true&w=majority"
```
6. Adicione a seguinte linha no final do [database.py](./src/database.py) na primeira vez para criar o seu usuário no banco de dados usando a sua conta da Bet 365:
```py
MongoDB.cadastrar("NOMEDOUSUARIO", "SENHA") # Nome do usuário da conta da Bet e sua senha
```
7. Inicie o [main.py](./main.py) e faça o login, e então retire a linha adicionada anteriormente.

![Config Video](./docs/images/configVideo.gif)
