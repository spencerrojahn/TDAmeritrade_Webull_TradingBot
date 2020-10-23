# Import needed modules
import email
import imaplib
import requests
from bs4 import BeautifulSoup
from webull import webull
import time as t
from datetime import datetime


running = False

# Get credentials
credentials = open("credentials.txt").read().splitlines()

# Login to Webull
wb = webull()
#wb.get_mfa(username=credentials[4])
wb.login(username=credentials[4], password=credentials[5], device_name="XXXXXXXXXXX", mfa="XXXXXX")
print(wb.get_account())

# Set up connection to email and login
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(credentials[2], credentials[3])

print("START PROGRAM")

# Program is constantly running
# CURRENT STRATEGY: start at 4:00am and stop at 7:58pm
while (1):

	# Print current time just to make sure that the program is running and so I can see where the
	# stock was either bought or sold
	print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


	if (int(datetime.now().hour)>=4 and int(datetime.now().hour)<20):

		if not running:
			print("START TRADING")
			running = True

		if (int(datetime.now().hour)==19 and int(datetime.now().minute)==58):
			print("STOP TRADING and PROGRAM")
			quit()

		try: 	
			# Get the most recent email from inbox
			mail.select("INBOX")
			result, data = mail.uid("search", None, "ALL")
			inbox_item_list = data[0].split()
			most_recent = inbox_item_list[-1]
			result2, email_data = mail.uid("fetch", most_recent, "(RFC822)")
			raw_email = email_data[0][1].decode("utf-8")
			email_message = email.message_from_string(raw_email)

			if (email_message["From"] == "alerts@thinkorswim.com"):
				
				# Get the body of email
				# TD Ameritrade sends email alerts with body as HTML
				html = email_message.get_payload()

				# Use Beautiful Soup to parse the html to get ticker and action
				soup = BeautifulSoup(html, "html.parser")
				alert_message = soup.p.text
				alert_message = alert_message.partition(":")[2]
				alert_message = alert_message.partition(":")[2]
				stocks = alert_message.partition("were")[0].replace(",", "")
				stocks_list = stocks.split()
				info = alert_message.partition("to")[2].replace(".", "")
				if "=" in stocks_list:
					stocks_list.remove("=")
					stocks_list.remove("was")
					stocks_list.remove("added")
					stocks_list.remove("to")
					if "Scan_BUY." in stocks_list:
						stocks_list.remove("Scan_BUY.")
					else:
						stocks_list.remove("Scan_SELL.")

				# THIS IS JUST FOR TESTING (LEAVE COMMENTED)
				# print("Stocks: " + str(stocks_list))
				# print(info)

				# Get current positions
				positions = open("positionsWebull.txt").read().splitlines()

				# If alert is a BUY alert for Webull strategy (Strategy 1)
				if "Scan_BUY" in info:

					for stock in stocks_list:
						
						# If I don't already have a position with the current stock (Webull)
						if stock not in positions:

							try:
								# Check if I have enough buying power for the share quantity
								wb.get_trade_token(password=credentials[6])
								buying_power = float(wb.get_account()["accountMembers"][3]["value"])

								wb.get_trade_token(password=credentials[6])
								last_price = float(wb.get_quote(stock=stock)["close"])
								position_total_est = last_price*102
								if (buying_power > position_total_est):

									# BUY Strategy 1 (Webull)
									wb.get_trade_token(password=credentials[6])
									wb.place_order(stock=stock, price=last_price+0.01, action="BUY", orderType="LMT", enforce="GTC", qty=100, outsideRegularTradingHour=True)
									print("BUY: "+ stock)

									# Append stock to positions.txt (Webull)
									with open("positionsWebull.txt", "a") as text_file:
										text_file.write(stock + "\n")				

							except Exception as e:
								print(str(e))
								continue

				# Else if the alert is a SELL alert for Webull strategy (Strategy 1) and Webull strategy (Strategy 2)
				if "Scan_SELL" in info:

					for stock in stocks_list:
							
						# If I have position with the current stock (Webull)
						if stock in positions:

							wb.get_trade_token(password=credentials[6])
							last_price = float(wb.get_quote(stock=stock)["close"])

							# SELL Strategy 1 (Webull)
							wb.get_trade_token(password=credentials[6])
							wb.place_order(stock=stock, price=last_price-0.01, action="SELL", orderType="LMT", enforce="GTC", qty=100, outsideRegularTradingHour=True)
							print("SELL: "+ stock)

							# Remove stock from positions (Webull)
							positions.remove(stock)

							# Print positions back to positions.txt (Webull)
							with open("positionsWebull.txt", "w") as text_file:
								for stock in positions:
									text_file.write(stock + "\n")

		except KeyboardInterrupt:
			print("\nQuitting program...")
			quit()

		except Exception as e:
			print(str(e))

			# Sleep program for 10 seconds 
			t.sleep(5)

			while (1):

				try:
					mail = imaplib.IMAP4_SSL("imap.gmail.com")
					mail.login(credentials[2], credentials[3])
					break
					
				except Exception as e:
					print(str(e))
					t.sleep(2)
					continue
			
			continue

	# Sleep program for 10 seconds 
	t.sleep(5)
	






