# Discord Cryptocurrency bot.
from requests import Request, Session
import discord
import json
import os

# Hidden keys
my_secret = os.environ['Token']
my_secret2 = os.environ['API_KEY']


client = discord.Client()

# url for Coinmarketcap.com lastest crypto updates.
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

@client.event
async def on_ready():
  # Verifies that the bot is on. 
  print('The Bot is on!'.format(client))


@client.event
async def on_message(message):

  if message.author == client.user:
    return

  # The bot is scanning for the period symbol, before any cryptocurrency symbol is given.
  if message.content.startswith('.'):
    
    name = message.content

    # The first character is removed, (the period).
    name = name[1:]

    parameters = {
      'symbol' : name,
      'convert' : 'USD'
    }

    headers = {
      'Accepts' : 'application/json',
      'X-CMC_PRO_API_KEY' : my_secret2  # API key
    }
    
    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    # This If-statement will check if the cryptocurrency symbol is listed on Coinmarketcap.com,
    # and if not it will return the error message to the discord server.
    if response:

      # Using the try command to test the block of code for anymore errors.
      try:
        # Sets the price of the cryptocurrency to the variable.
        price = (json.loads(response.text)['data'][name.upper()]['quote']['USD']['price'])

      except KeyError:
        # Error message for a Cryptocurrency listed on Coinmarketcap.com, but doesn't have any data listed for it.  
        await message.channel.send("Data for " + name.upper() + " isn't available on Coinmarketcap.com")
        return
      
      # Rounds to 2 decimals places if the price is greater than or equal to 0.1
      if (price >= 0.1):
        price = str(round(price, 2))

      # Prints the price of the Cryptocurrency.
      await message.channel.send("Price of " + name.upper() + " is:" + " ${0}".format(price))
      
    else:
      # Error message for a Cryptocurrency not listed on Coinmarketcap.com 
      await message.channel.send("This isn't a Cryptocurrency!\nOr it's not listed on Coinmarketcap.com")
      return


client.run(my_secret) # Discord Token