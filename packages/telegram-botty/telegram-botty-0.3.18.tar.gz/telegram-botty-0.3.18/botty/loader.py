from botty_core import App, Texts, env

BOT_TOKEN = env.get("BOT_TOKEN")
TEXTS_PATH = env.get("TEXTS_PATH")

app = App(BOT_TOKEN)
texts = Texts(TEXTS_PATH)
