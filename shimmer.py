import os
import logging
import interactions
from dotenv import load_dotenv
from interactions import *
from rollcall import *

rollcall_history = RollcallHistory()
current_id = 1

@slash_command(name="notif", description="Notify a user")
@slash_option(name="user", description="User to notify", opt_type=OptionType.USER, required=True)
@slash_option(name="text", description="Text to send", opt_type=OptionType.STRING, required=True)
@slash_option(name="times", description="Number of times to send", opt_type=OptionType.INTEGER, required=False)
async def notif(ctx: SlashContext, user: User, text: str, times = 5):
    await ctx.respond(f"Sending {text} to {user.mention} {times} times")
    if times > 10: times = 10
    for _ in range(times):
        await user.send(text)

rollcall_components = spread_to_rows(
    Button(
        custom_id="hitters", label="Hitter", style=ButtonStyle.PRIMARY
    ),
    Button(
        custom_id="setters", label="Setter", style=ButtonStyle.PRIMARY
    ),
    Button(
        custom_id="rally", label="Rally Dragon", style=ButtonStyle.DANGER
    ),
    Button(
        custom_id="reset", label="No longer available", style=ButtonStyle.SECONDARY
    )
)
@slash_command(name="rollcall")
@slash_option(name="coords", description="Coordinates for the rollcall", opt_type=OptionType.STRING, required=False)
async def rollcall(ctx: SlashContext, coords: str = ""):
    global current_id
    rollcall = Rollcall(id=current_id, timestamp=time.time(), coords=coords)
    await ctx.respond(content=rollcall.generate_rollcall_prompt(), embed=rollcall.generate_rollcall_embed(), components=rollcall_components)
    rollcall_history.add_rollcall(rollcall)
    current_id += 1
        
@component_callback("hitters")
async def set_hitter(ctx: ComponentContext):
    rollcall = rollcall_history.get_rollcall_from_embed_title(ctx.message.embeds[0].title)
    rollcall.set_user_as_hitter(ctx.member)
    await ctx.edit_origin(content=rollcall.generate_rollcall_prompt(), embed=rollcall.generate_rollcall_embed(), components=rollcall_components)
    rollcall_history.set_rollcall(rollcall)


@component_callback("setters")
async def set_setter(ctx: ComponentContext):
    rollcall = rollcall_history.get_rollcall_from_embed_title(ctx.message.embeds[0].title)
    rollcall.set_user_as_setter(ctx.member)
    await ctx.edit_origin(content=rollcall.generate_rollcall_prompt(), embed=rollcall.generate_rollcall_embed(), components=rollcall_components)
    rollcall_history.set_rollcall(rollcall)

@component_callback("rally")
async def set_rallied(ctx: ComponentContext):
    rollcall = rollcall_history.get_rollcall_from_embed_title(ctx.message.embeds[0].title)
    rollcall.set_user_as_rallied(ctx.member)
    await ctx.edit_origin(content=rollcall.generate_rollcall_prompt(), embed=rollcall.generate_rollcall_embed(), components=rollcall_components)
    rollcall_history.set_rollcall(rollcall)

@component_callback("reset")
async def reset_user(ctx: ComponentContext): 
    rollcall = rollcall_history.get_rollcall_from_embed_title(ctx.message.embeds[0].title)
    rollcall.reset_user(ctx.member)
    await ctx.edit_origin(content=rollcall.generate_rollcall_prompt(), embed=rollcall.generate_rollcall_embed(), components=rollcall_components)
    rollcall_history.set_rollcall(rollcall)

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    cls_log = logging.getLogger(interactions.const.logger_name)
    cls_log.setLevel(logging.INFO)

    TOKEN = os.getenv("TOKEN")
    bot = Client(intents=Intents.DEFAULT)
    bot.start(TOKEN)
