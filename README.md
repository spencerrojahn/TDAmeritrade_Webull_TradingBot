# TDAmeritrade_Webull_TradingBot
Used to trade stocks automatically on the broker Webull based on your preferred algorithm alerts from TD Ameritrade's platform Thinkorswim.

MUST have a TD Ameritrade account and a Webull account in order to use this program.

The tradingBotWebull.py contains all of the source code for the program. You will need to provide your own credentials for the Webull login and the email login that is connected to your TD Ameritrade's Thinkorswim alerts. The credentials.txt shows how you should orient your credentials, the tradingBotWebull.py file uses credentials.txt to retrieve your credentials.

PROGRAM: 
This program simply buys or sells 100 shares of whatever stock your alogrithm from TD Ameritrade's Thinkorswim alerts you to buy or sell. It will also maintain a text file containing the stock that you current hold. It will run from pre-market open, for me 4am EST, to post-market close, for me 8pm EST. It sleeps every 10 seconds because this program is meant for a swing-trading strategy, meaning that we don't need data being collected constantly, we can take 10 second breaks.
