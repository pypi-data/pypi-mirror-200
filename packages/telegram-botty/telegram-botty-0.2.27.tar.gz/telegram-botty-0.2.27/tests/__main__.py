from botty import CompositeHandler, StartGroupHandler, StartHandler, TextContext, app
from botty.handlers import CommandHandler


async def start_callback(ctx: TextContext) -> None:
    await ctx.reply("start")


async def start_group_callback(ctx: TextContext) -> None:
    await ctx.reply("startgroup")


async def test_callback(ctx: TextContext) -> None:
    await ctx.reply("test")


h1 = StartHandler(start_callback)
h2 = StartGroupHandler(start_group_callback)
h3 = CommandHandler("test", test_callback)
handler = CompositeHandler(h2, h1)
handler = CompositeHandler(handler, h3)

app.run(handler)
