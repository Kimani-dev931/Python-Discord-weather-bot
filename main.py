# import the discord library which allows you to interact with discord platform
import discord
# imports the 'commands' module from the discord.ext package, which provides extra functionality for building bot commands.
from discord.ext import commands
# imports the 'requests' library, which allows us to send HTTP requests to APIs.
import requests
# imports the 'aiohttp' library, which provides support for asynchronous HTTP requests.
import aiohttp

# defines a constant variable 'API_KEY' that holds the Weather API key to use for retrieving weather information.
API_KEY = "e000df0cc8d04cee952143658230204"
# creates a new Discord bot client object with all available intents enabled.
client = discord.Client(intents=discord.Intents.all())


# prints a message to the console indicating that the bot has successfully connected to the Discord server.
@client.event
async def on_ready():
    print("The weather Bot has connected to Discord server!")


@client.event
# defines an asynchronous function that is called whenever a new message is sent to the Discord server.
async def on_message(message):
    # checks if the message is sent by the bot itself and returns if true, so the bot won't respond to its own messages.
    if message.author == client.user:
        return

    prefix_list = ['!w-','w.']  # List of prefixes to check for at the beginning of incoming messages to identify whether the user is requesting a weather report.

    # Check if message starts with any of the prefixes
    # initializes the 'prefix_used' variable to None
    prefix_used = None
    # iterates over each prefix in the prefix_list
    for prefix in prefix_list:
        # checks if the incoming message starts with the current prefix.
        if message.content.startswith(prefix):
            # sets the prefix_used variable to the current prefix if the message starts with it.
            prefix_used = prefix
            # exits the loop once a matching prefix is found.
            break
    # checks if none of the prefixes matched the incoming message.
    if not prefix_used:
        # checks if the incoming message is either 'w.?' or '!w?'.
        if message.content in ['w.?', '!w?']:
            # defines a string variable 'help_message' that holds the help message for the bot.
            help_message = "To use this weather bot, type one of the following commands followed by a city name:\n\n"
            help_message += "!w-<city> : Get the weather for <city> in degrees Celsius and Fahrenheit.\n"
            help_message += "w.<city> : Get the weather for <city> in degrees Celsius and Fahrenheit.\n\n"
            help_message += "Example: `!w-London` or `w.Paris`"
            # sends the help message to the channel where the message was received.
            await message.channel.send(help_message)
            # exits the function.
            return

        # If neither prefix nor help command is found, ignore the message
        return

    # extracts the city name from the incoming message by removing the prefix and any leading/trailing spaces.
    city = message.content[len(prefix_used):].strip()

    # defines the URL for the Weather API.
    url = "http://api.weatherapi.com/v1/current.json"
    # defines a dictionary of parameters to send to the Weather API, including the API key and the requested city.
    params = {
        "key": API_KEY,
        "q": city
    }
    # creates a new asynchronous HTTP session object.
    async with aiohttp.ClientSession() as session:
        # sends an asynchronous HTTP GET request to the Weather API with the
        async with session.get(url, params=params) as res:
            if res.status == 400:
                await message.channel.send(f"City '{city}' not found.")
                return

            data = await res.json()
            # Extract the following weather information from the weather API
            location = data["location"]["name"]
            temp_c = data["current"]["temp_c"]
            temp_f = data["current"]["temp_f"]
            humidity = data["current"]["humidity"]
            wind_kph = data["current"]["wind_kph"]
            wind_mph = data["current"]["wind_mph"]
            condition = data["current"]["condition"]["text"]
            image_url = "http:" + data["current"]["condition"]["icon"]

            embed = discord.Embed(title=f"Weather for {location}",
                                  description=f"The condition in '{location}' is '{condition}'")
            embed.add_field(name="Temperature", value=f"c:{temp_c}  | F:{temp_f}")
            embed.add_field(name="Humidity", value=f"{humidity}")
            embed.add_field(name="wind speeds", value=f"KPH:{wind_kph}  | MPH:{wind_mph}")
            embed.set_thumbnail(url=image_url)

            await message.channel.send(embed=embed)


client.run("MTA5MTg0MjE1NzA0NTg4MzAxMA.Gq5mWA.h0Dd_X3hrr0WC2PpPvwc_bW27TC5iy9N3Sa2qI")
