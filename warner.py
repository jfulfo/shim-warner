import os
import logging
import interactions
from dotenv import load_dotenv
from interactions import Client, slash_command, slash_option, OptionType, SlashContext, Intents, User, Button, ButtonStyle, ActionRow, spread_to_rows, listen

load_dotenv()
logging.basicConfig()
cls_log = logging.getLogger(interactions.const.logger_name)
cls_log.setLevel(logging.DEBUG)

TOKEN = os.getenv("TOKEN")
bot = Client(intents=Intents.DEFAULT)

hitters = []
sop_setters = []
keep_setters = []

@slash_command(name="notif", description="Notify a user")
@slash_option(
    name="user",
    description="The user to notify",
    opt_type=OptionType.USER,
    required=True
)
@slash_option(
    name="text",
    description="The text to notify the user with",
    opt_type=OptionType.STRING,
    required=True
)
@slash_option(
    name="times",
    description="The number of times to notify the user",
    opt_type=OptionType.INTEGER,
    required=False
)
async def notif(ctx: SlashContext, user: User, text: str, times: int = 5):
    await ctx.respond(f"Notifying {user.mention} with \"{text}\" {times} times")

    for _ in range(times):
        await user.send(f"{text}")

components: list[ActionRow] = spread_to_rows(
    Button(style=ButtonStyle.PRIMARY,custom_id="hitters",label="Hitter",disabled=False),
    Button(style=ButtonStyle.PRIMARY,custom_id="sop_setters",label="SOP Setter",disabled=False),
    Button(style=ButtonStyle.PRIMARY,custom_id="keep_setters",label="Keep Setter",disabled=False)
)

@listen()
async def on_component(event):
    ctx = event.ctx
    if ctx.author.user.mention in hitters:
        hitters.remove(ctx.author.user.mention)
    elif ctx.author.user.mention in sop_setters:
        sop_setters.remove(ctx.author.user.mention)
    elif ctx.author.user.mention in keep_setters:
        keep_setters.remove(ctx.author.user.mention)

    match ctx.custom_id:
        case "hitters":
            hitters.append(ctx.author.user.mention)
        case "sop_setters":
            sop_setters.append(ctx.author.user.mention)
        case "keep_setters":
            keep_setters.append(ctx.author.user.mention)

    await ctx.edit_origin(content=f"**Please react to your respective button if you are online and available:**\n\nHitter: {', '.join(hitters)}\nSOP Setter: {', '.join(sop_setters)}\nKeep Setter: {', '.join(keep_setters)}", components=components)

@slash_command(name="rollcall", description="Perform a rollcall")
async def rollcall(ctx: SlashContext):
    response = await ctx.respond("**Please react to your respective button if you are online and available:**\n\nHitter:\nSOP Setter:\nKeep Setter:", components=components)

if __name__ == "__main__":
    print("Starting bot...")
    bot.start(TOKEN)

    
