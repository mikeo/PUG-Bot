import discord
from discord.ext.commands import Bot
from utils.config import bot_token
from discord_slash import SlashCommand

# Importing files from the commands directory to be initialised
from commands.BaseCommands import BaseCommands
from commands.RegistrationCommands import RegistrationCommands
from commands.CTFCommands import CTFCommands
from commands.EventCommands import EventCommands

intents = discord.Intents.all()

# Creating the bot object
bot = Bot(command_prefix="-", intents=intents)


@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.competing, name="PUG Season 2"))

    SlashCommand(bot, sync_commands=True)

    # Adding commands to the bot now that its ready
    bot.add_cog(BaseCommands(bot))
    bot.add_cog(RegistrationCommands(bot))
    bot.add_cog(CTFCommands(bot))
    bot.add_cog(EventCommands(bot))


bot.run(bot_token)
