from botty import CommandHandler, CompositeHandler, QueryHandler, StartHandler, app

handler = CompositeHandler(
    StartHandler("Hello"),
    CommandHandler("help", "Help"),
    QueryHandler(reply_text="?"),
)

app.run(handler)
