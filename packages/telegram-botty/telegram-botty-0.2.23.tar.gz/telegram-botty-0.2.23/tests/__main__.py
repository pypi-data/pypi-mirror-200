from botty import CompositeHandler, app
from botty.handlers import CommandReplyHandler, QueryReplyHandler, StartReplyHandler

handler = CompositeHandler(
    StartReplyHandler("Hello"),
    CommandReplyHandler("help", "Help"),
    QueryReplyHandler(text="?"),
)

app.run(handler)
