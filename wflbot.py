from pickle import TRUE
import discord, asyncio
from discord import app_commands

from wfltoken import get_token
from wfltoken import get_guild
from wfltoken import get_general
from wfltoken import get_botcommands

from heightroll import roll_height

guild = get_guild()
general = get_general()
botcommands = get_botcommands()

# for stats
default_season = 1

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            await tree.sync(guild = discord.Object(id = 1004183670086713445))
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

# To restrict to main server use as a command argument: , guild=discord.Object(id=guild)

# roll command
@tree.command(name="roll", description="Roll a height using the IBL odds", guild=discord.Object(id=guild))
@app_commands.choices(archetype=[
    app_commands.Choice(name="Tiny", value="tiny"),
    app_commands.Choice(name="Normal", value="normal"),
    app_commands.Choice(name="Giant", value="giant"),
    app_commands.Choice(name="Random", value="random"),
    ])
async def roll(interaction: discord.Interaction, archetype: app_commands.Choice[str]):
    await interaction.response.defer()
    await asyncio.sleep(1)
    await interaction.followup.send(roll_height(archetype.value))

client.run(get_token())