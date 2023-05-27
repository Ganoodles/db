"""The main entry point of the bot."""
import asyncio
import sys
import traceback
from datetime import datetime
import pathlib

import discord
from discord.ext import commands
import dotenv
import os

from tortoise import Tortoise

from src.utils.logger import Logger
import src.models as models 

intents = discord.Intents.all()


class BotHandler(commands.Bot):
    """The bot handler class."""
    
    def __init__(self):
        """Intializes `BotHandler`."""
        dotenv_path = '.env'
        dotenv.load_dotenv(dotenv_path)
         
        self.token = os.getenv('TOKEN')
        self.prefix = os.getenv('PREFIX')
        self.launch_time = datetime.utcnow()
        self.owner_ids = [int(id) for id in os.getenv('OWNER_IDS').split(',')]
        self.disabled_cogs = [str(cog) for cog in os.getenv('DISABLED_COGS').split(',')]
        self.default_activity = self.get_default_activity()
        self.logger = Logger()

        super().__init__(
            command_prefix=None,
            intents=intents,
            reconnect=True,
            activity=self.default_activity
        )

        # intialize the database
        asyncio.run(self.initialize_database())

        # starts the bot
        asyncio.run(self.bot_startup())


    def get_default_activity(self):
        """Sets the default activity."""
        return discord.Activity(
            type=discord.ActivityType.watching,
            name="you"
        )

    async def initialize_database(self):
        self.logger.debug("Initializing database...")
        
        await Tortoise.init(db_url='sqlite://data/db.sqlite3',
                            modules={'models': ['src.models']})

        await Tortoise.generate_schemas()
        
        self.logger.debug("Success - Database initialized")


    def run(self):
        """Runs the bot."""
        try:
            self.logger.debug("Logging in...")
            asyncio.run(self.start(self.token))
        except KeyboardInterrupt:
            self.logger.critical('Keyboard interruption detected, exiting...')
            asyncio.run(Tortoise.close_connections())
            asyncio.run(self.close())
        except Exception:
            traceback.print_exc(file=sys.stderr)


    async def on_ready(self):
        """Executes when the bot is ready."""
        assert self.user
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

        bot_guilds = self.guilds

        # adds all new servers to the database
        for guild in bot_guilds:
            server = await models.Server.get_or_none(id=guild.id)
            if not server:
                server = models.Server(id=guild.id)
                await server.save()

    async def bot_startup(self):
        """Blocking method that facilitates loading of all the bot's cogs along with any other preliminary setup."""
        self.logger.debug("Loading cogs...")

        # load all cogs inside the cogs folder
        cog_files = pathlib.Path("src/cogs").rglob("*.py")

        for cog in cog_files:
            try:
                cog_name = cog.stem
                if cog_name in self.disabled_cogs:
                    self.logger.debug(f"DISABLED - {cog_name}")
                    continue
                await self.load_extension(f"src.cogs.{cog_name}")
                self.logger.debug(f"LOADED - {cog_name}")
            except Exception as e:
                self.logger.error(f"Failed to load cog {cog_name}: {e}")


def main():
    """Entry point for the application."""
    BotHandler().run()


if __name__ == '__main__':
    main()
