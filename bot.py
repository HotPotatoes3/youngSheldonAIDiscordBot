import os
import shutil
import uuid
import PIL.Image
import discord
from discord.ext import commands
import requests
import responses



def run_discord_bot(discord):

    TOKEN = os.environ['TOKEN']

    app_commands = discord.app_commands
    bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
    bot.remove_command("help")

    @bot.event
    async def on_ready():
        print("Slash Commands working")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
            for i in synced:
                print(i)
        except Exception as e:
            print(e)
    @bot.event
    async def on_message(message):
        if message.author != bot.user:
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            print(f"{username} said: '{user_message}' ({channel})")
            await bot.process_commands(message)



    # NON-SLASH COMMAND

    @bot.command()
    async def help(ctx):
        await ctx.message.reply(responses.ai_response("help", None, None))

    @bot.command()
    async def asksheldon(ctx):
        try:
            input = ctx.message.content[10:]
            resp = responses.ai_response("asksheldon", input, None)
            await ctx.message.reply(resp)
        except Exception as e:
            print(e)
            await ctx.message.reply("Please check your input and try again")

    @bot.command()
    async def asksheldonpro(ctx):
        imageName = ''
        try:
            input = ctx.message.content[12:]
            r = requests.get(ctx.message.attachments[0], stream=True)
            imageName = str(uuid.uuid4()) + '.jpg'
            with open(imageName, 'wb') as out_file:
                print('Saving image: ' + imageName)
                shutil.copyfileobj(r.raw, out_file)
            img = PIL.Image.open(imageName)
            resp = responses.ai_response('asksheldon2',input, img)
            os.remove(imageName)
            await ctx.message.reply(resp)
        except Exception as e:
            print(e)
            await ctx.message.reply(
                "An error occured, please try again, or contact the developer if this issue persists.")
            os.remove(imageName)





    # SLASH COMMANDS
    @bot.tree.command(name='asksheldon', description='Responds as Sheldon Cooper from Young Sheldon')
    @app_commands.describe(input="What do you want to ask/tell sheldon?")
    async def asksheldon(interaction: discord.Interaction, input: str):
        try:
            await interaction.response.defer()
            resp = responses.ai_response("asksheldon", input, None)
            await interaction.followup.send(resp)
        except Exception as e:
            print(e)
            await interaction.response.send_message("Failed")

    @bot.tree.command(name='asksheldonpro', description='Responds to text input + images Sheldon Cooper from Young Sheldon')
    @app_commands.describe(input="What do you want to ask/tell sheldon?")
    async def asksheldon2(interaction: discord.Interaction, input: str, file: discord.Attachment):
        imageName = ''
        try:
            await interaction.response.defer()
            r = requests.get(file, stream=True)
            imageName = str(uuid.uuid4()) + '.jpg'
            with open(imageName, 'wb') as out_file:
                print('Saving image: ' + imageName)
                shutil.copyfileobj(r.raw, out_file)
            img = PIL.Image.open(imageName)
            resp = responses.ai_response('asksheldon2',input, img)
            await interaction.followup.send(resp)
            os.remove(imageName)
        except Exception as e:
            print(e)
            await interaction.followup.send(
                "An error occured, please try again, or contact the developer if this issue persists.")
            os.remove(imageName)

    @bot.tree.command(name='help', description='List commands (non-slash commands)')
    async def help(interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            resp = responses.ai_response("help", None, None)
            await interaction.followup.send(resp)
        except Exception as e:
            print(e)
            await interaction.response.send_message("Failed")

    bot.run(TOKEN)
