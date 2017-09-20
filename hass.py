import discord
from discord.ext import commands
import homeassistant.remote as remote
import re

"""Written by Just_Insane"""

api = remote.API('', '')
url = ''

class Hass:

    def __init__(self, bot):
        self.bot = bot
        self.session = self.bot.http.session

    @commands.command()
    async def on(self, entity : str, brightness : str):
        try:
            domain = 'light'
            state = 'turn_on'
            remote.call_service(api, domain, state, {'entity_id': '{}'.format(domain) + '.{}'.format(entity), 'brightness': '{}'.format(brightness)})
        except:
            await self.bot.say("There was an error!")

    @commands.command()
    async def off(self, entity: str):
        try:
            domain = 'light'
            state = 'turn_off'
            remote.call_service(api, domain, state, {'entity_id': '{}'.format(domain) + '.{}'.format(entity)})
        except:
            await self.bot.say("There was an error!")

    @commands.command()
    async def state(self, entity : str):
        try:
            domain = 'light'
            ent = remote.get_state(api, domain + '.{}'.format(entity))
            await self.bot.say('{} is {}.'.format(ent.name, ent.state))
        except:
            await self.bot.say("There was an error!")

    @commands.command()
    async def hass(self, task : str):
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

def setup(bot):
    n = Hass(bot)
    bot.add_cog(n)
