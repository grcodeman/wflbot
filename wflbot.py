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

from wflbank import grab_bal, grab_teambal

guild = get_guild()
general = get_general()
botcommands = get_botcommands()

# for stats
default_season = 1

link_perms = ["395724838620102658","1002315735730770060","410252795757723650"]

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
@tree.command(name="bal", description="View a player's Balance and AC Status", guild=discord.Object(id=guild))
async def self(interaction: discord.Interaction, player: str=None):
    await interaction.response.defer()
    if (player == None):
        player = get_playerid(str(interaction.user.id))
    if (player != "Error"):
        try:
            info = grab_bal(int(player))
            info = info.split(",")
            await interaction.followup.send("**" + info[2] + " (" + str(player) + ")** \nBal: " + info[0] + "UP\nAC: " + info[1])
        except:
            await interaction.followup.send("Process Failed: Missing player ID")
    else:
        await interaction.followup.send("This account has not been linked yet.")

# teambal command
@tree.command(name="teambal", description="View a team's Balance and AC Status", guild=discord.Object(id=guild))
@app_commands.choices(team=[
    app_commands.Choice(name="UCD Dublin", value="1"),
    app_commands.Choice(name="Ulsan Hyundai FC", value="2"),
    app_commands.Choice(name="Dinamo Zagreb", value="3"),
    app_commands.Choice(name="TSG Hoffenheim", value="4"),
    app_commands.Choice(name="Inter Miami CF", value="5"),
    app_commands.Choice(name="Sporting KC", value="6"),
    app_commands.Choice(name="Manchester United", value="7"),
    app_commands.Choice(name="AC Milan", value="8"),
    ])
async def viewbal(interaction: discord.Interaction, team: app_commands.Choice[str]):
    await interaction.response.defer()
    if (interaction.channel_id == general):
        await interaction.followup.send("Go to <#" + str(botcommands) + ">")
    else:
        try:
            value = grab_teambal(team.value)
            text = ""
            current = 0
            players = value.split(":")
            for i in players:
                info = i.split(",")
                if current > 0:
                    text += "\n"
                text += "**" + info[6] + " (" + info[0] + ")** | Bal: **" + info[4] + "UP** AC: **"  + info[5] + "**"
                current += 1
            teamembed = discord.Embed(title=(team.name + " (" + team.value + ")"), description=text)
            teamembed.set_footer(text=("Requested by " + interaction.user.name))
            await interaction.followup.send(embed=teamembed)
        except:
            await interaction.followup.send("Process Failed")

client.run(get_token())