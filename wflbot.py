from pickle import TRUE
import discord, asyncio
from discord import app_commands

from wfltoken import get_token
from wfltoken import get_guild
from wfltoken import get_general
from wfltoken import get_botcommands

from wfldb import add_playerid
from wfldb import get_playerid

from submitform import submit_ac

from heightroll import roll_height

from wflbank import grab_bal

guild = get_guild()
general = get_general()
botcommands = get_botcommands()

# for stats
default_season = 1

link_perms = ["395724838620102658","1002315735730770060"]

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            await tree.sync(guild = discord.Object(id = guild))
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

# link command
@tree.command(name="link", description="Admin can link user account to player id", guild=discord.Object(id=guild))
async def self(interaction: discord.Interaction, player: str, user: discord.Member):
    await interaction.response.defer()
    if (str(interaction.user.id) in link_perms):
        disc_id = str(user.id)
        player_id = str(player)
        add_playerid(disc_id, player_id)
        await interaction.followup.send("Linked: `" + disc_id + "` to `" + player_id + "`")
    else:
        await interaction.followup.send("You do not have permission to use this command.")

# ac command
@tree.command(name="ac", description="Submit an Activity Check (Weekly Checkin)", guild=discord.Object(id=guild))
async def self(interaction: discord.Interaction):
    await interaction.response.defer()
    player = get_playerid(str(interaction.user.id))
    if (player != "Error"):
        await interaction.followup.send(submit_ac(interaction.user.id, player, (interaction.user.name + "#" + interaction.user.discriminator)))
    else:
        await interaction.followup.send("This account has not been linked yet.")

# bal command
@tree.command(name="bal", description="View a players Balance and AC Status", guild=discord.Object(id=guild))
async def self(interaction: discord.Interaction, player: str=None):
    await interaction.response.defer()
    if (player == None):
        player = get_playerid(str(interaction.user.id))
    if (player != "Error"):
        info = grab_bal(int(player))
        info = info.split(",")
        await interaction.followup.send("**" + info[2] + " (" + str(player) + ")** \nBal: " + info[0] + "UP\nAC: " + info[1])
    else:
        await interaction.followup.send("This account has not been linked yet.")

client.run(get_token())