## [BetBot](https://github.com/JDaniloC/Individual-Bet365Bot)

![BetBot Video](../images/video.gif)

> I'm not responsible for the use of this project

## What's needed to run the project
- Firefox with Gecko Driver installed
- Python with the dependencies listed in requirements.txt
- MongoDB cluster with a Collection called users
- Bet365 account to enter in the web site

## Como rodar o projeto
1. Install python 3.9, and at the root of the project install the [dependencies](../requirements.txt):
```bash
pip install -r requirements.txt
```
2. Make sure you have an account at [Bet 365](https://www.bet365.com/), and tget your username and password.
3. Make sure you have the [Firefox](../src/widgets.py) installed with the [Gecko Driver](https://www.take.net/blog/wp-content/cache/wp-rocket/take.net/blog/take-test/instalacao-geckodriver-driver-para-abrir-o-firefox-no-selenium/index-https.html_gzip) in case of FirefoxBrowser, or just use the ChromeBrowser in the [bot.py](../src/bot.py) with the chromedriver.
4. Create an account at [MongoDB](https://medium.com/reprogramabr/conectando-no-banco-de-dados-cloud-mongodb-atlas-bca63399693f#:~:text=Acesse%20ao%20site%20do%20MongoDB,esquerdo%2C%20clique%20em%20Database%20Access.), and a database called [betbot](../src/database.py) with a Collection called users.
5. Create a file at the root of the project called env.py with your's Mongo's [authentication](https://docs.atlas.mongodb.com/tutorial/connect-to-your-cluster/), without the <> ([#12](https://github.com/JDaniloC/Individual-Bet365Bot/issues/12)):
```py
autenticacao = "mongodb+srv://<MONGOUSER>:<MONGOPASSWORD>@cluster<CLUSTERID>.mongodb.net/betbot?retryWrites=true&w=majority"
```
6. Add the following line at the end of the [database.py](../src/database.py) in the first time, to create your user in the database using you Bet365 account:
```py
MongoDB.cadastrar("USERNAME", "PASSWORD") # Nome do usuário da conta da Bet e sua senha
```
7. Run the [main.py](../main.py) and login, removing the line added before.

![Config Video](../images/configVideo.gif)
