from botty import CompositeHandler, app
from botty.handlers import CommandReplyHandler, StartReplyHandler

handler = CompositeHandler(
    StartReplyHandler("Hello"),
    CommandReplyHandler("help", "Help"),
)

app.run(handler)
