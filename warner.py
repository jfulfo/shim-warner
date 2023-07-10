import os
import logging
import interactions
from dotenv import load_dotenv
from interactions import Client, slash_command, slash_option, OptionType, SlashContext, Intents, User

load_dotenv()
logging.basicConfig()
cls_log = logging.getLogger(interactions.const.logger_name)
cls_log.setLevel(logging.DEBUG)

TOKEN = os.getenv("TOKEN")
bot = Client(intents=Intents.DEFAULT)


@slash_command(name="notif", description="notify a user")
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

if __name__ == "__main__":
    print("Starting bot...")
    bot.start(TOKEN)

