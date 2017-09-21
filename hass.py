from cogs.utils.dataIO import dataIO
# from .utils import 
from __main__ import send_cmd_help
from __main__ import settings as bot_settings
# Sys.
import discord
from discord.ext import commands
import homeassistant.remote as remote
import re
import json
import os

"""Written by Just_Insane"""

DIR_DATA = "data/hass"
SETTINGS = DIR_DATA+"/settings.json"
DEFAULT = {"ip": "","api_key": ""}
api = remote.API("", "")
url = ""

class Hass:

    def __init__(self, bot):
        self.bot = bot
        self.session = self.bot.http.session
        self.settings = dataIO.load_json(SETTINGS)
        if self.settings["ip"] == "":
            print("Cog error: hass, no IP found, please configure me!")
        if self.settings["api_key"] == "":
            print("Cog error: hass, no API Key found, please configure me!")
        global api
        global url
        api = remote.API(self.settings["ip"], self.settings["api_key"])
        url = 'https://hass.justin-tech.com'

    @commands.command()
    async def on(self, entity : str, brightness : str):
        """Turn a light on"""
        try:
            domain = 'light'
            state = 'turn_on'
            remote.call_service(api, domain, state, {'entity_id': '{}'.format(domain) + '.{}'.format(entity), 'brightness': '{}'.format(brightness)})
        except:
            await self.bot.say("There was an error!")

    @commands.command()
    async def off(self, entity: str):
        """Turn a light off"""
        try:
            domain = 'light'
            state = 'turn_off'
            remote.call_service(api, domain, state, {'entity_id': '{}'.format(domain) + '.{}'.format(entity)})
        except:
            await self.bot.say("There was an error!")

    @commands.command()
    async def state(self, entity : str):
        """Get the state of a light"""
        try:
            domain = 'light'
            ent = remote.get_state(api, domain + '.{}'.format(entity))
            await self.bot.say('{} is {}.'.format(ent.name, ent.state))
        except:
            await self.bot.say("There was an error!")

    @commands.command()
    async def hass(self, task : str):
        """Other HASS Commands"""
        if task == 'help':
            await self.bot.say("**Home Assistant Bot!**\n\n**The commands are:**\n\n**[p]hass help** - Print this Help\n**[p]hass climate** - output climate infromations\n**[p]hass lights** - output state of all lights\n**[p]on** - Turn on a light\n**[p]off** - Turn off a light")
        elif task == 'climate':
            ent = remote.get_state(api, 'group.climate')
            entstr = '{}'.format(ent)
            # regex help provided by Python help discord server
            ents = re.findall(r"\W(s[e,u].[^']+)", entstr)
            embed = discord.Embed(title="HASS climate", url=url, description="Climate at home", color=3447003)
            for i in ents:
                climate = remote.get_state(api, '{}'.format(i))
                try:
                    embed.add_field(name='{}'.format(climate.name), value='{} {}'.format(climate.state, climate.attributes['unit_of_measurement']), inline=False)
                except:
                    break
            embed.set_footer(text="HASS")
            await self.bot.say(embed=embed)
        elif task == 'lights':
            ent = remote.get_state(api, 'group.all_lights')
            entstr = '{}'.format(ent)
            # regex help provided by Python help discord server
            ents = re.findall(r"\W(light\.[^']+)", entstr)
            embed = discord.Embed(title="HASS lights", url=url, description="Lights at home", color=3447003)
            for i in ents:
                lights = remote.get_state(api, '{}'.format(i))
                try:
                    # zero width char to to get around lack of support for no value field
                    embed.add_field(name='{} {}'.format(lights.name, lights.state), value='\u200b', inline=False)
                except:
                    break
            embed.set_footer(text="HASS")
            await self.bot.say(embed=embed)

        else:
            await self.bot.say("**Home Assistant Bot!**\n\n**The commands are:**\n\n**[p]hass help** - Print this Help\n**[p]hass climate** - output climate infromations\n**[p]hass lights** - output state of all lights\n**[p]on** - Turn on a light\n**[p]off** - Turn off a light")

    @commands.command(pass_context=True)
    async def apikey_hass(self, ctx, key):
        """Set the hass API key."""
        user = ctx.message.author
        if self.settings["api_key"] != "":
            await self.bot.say("{} ` hass API key found, overwrite it? y/n`".format(user.mention))
            response = await self.bot.wait_for_message(author=ctx.message.author)
            if response.content.lower().strip() == "y":
                self.settings["api_key"] = key
                dataIO.save_json(SETTINGS, self.settings)
                await self.bot.say("{} ` hass API key saved...`".format(user.mention))
            else:
                await self.bot.say("{} `Cancled API key opertation...`".format(user.mention))
        else:
            self.settings["api_key"] = key
            dataIO.save_json(SETTINGS, self.settings)
            await self.bot.say("{} ` hass API key saved...`".format(user.mention))
        self.settings = dataIO.load_json(SETTINGS)

    @commands.command(pass_context=True)
    async def ip_hass(self, ctx, ip):
        """Set the hass IP."""
        user = ctx.message.author
        if self.settings["ip"] != "":
            await self.bot.say("{} ` hass IP found, overwrite it? y/n`".format(user.mention))
            response = await self.bot.wait_for_message(author=ctx.message.author)
            if response.content.lower().strip() == "y":
                self.settings["ip"] = key
                dataIO.save_json(SETTINGS, self.settings)
                await self.bot.say("{} ` hass IP saved...`".format(user.mention))
            else:
                await self.bot.say("{} `Cancled IP opertation...`".format(user.mention))
        else:
            self.settings["ip"] = ip
            dataIO.save_json(SETTINGS, self.settings)
            await self.bot.say("{} ` hass IP saved...`".format(user.mention))
        self.settings = dataIO.load_json(SETTINGS)

def check_folders():
    if not os.path.exists(DIR_DATA):
        print("Creating data/hass folder...")
        os.makedirs(DIR_DATA)

def check_files():
    if not os.path.isfile(SETTINGS):
        print("Creating default hass settings.json...")
        dataIO.save_json(SETTINGS, DEFAULT)
    else:  # Consistency check
        try:
            current = dataIO.load_json(SETTINGS)
        except JSONDecodeError:
            dataIO.save_json(SETTINGS, DEFAULT)
            current = dataIO.load_json(SETTINGS)

        if current.keys() != DEFAULT.keys():
            for key in DEFAULT.keys():
                if key not in current.keys():
                    current[key] = DEFAULT[key]
                    print( "Adding " + str(key) + " field to imdb settings.json")
            dataIO.save_json(SETTINGS, DEFAULT)

def setup(bot):
    check_folders()
    check_files()
    n = Hass(bot)
    bot.add_cog(n)
