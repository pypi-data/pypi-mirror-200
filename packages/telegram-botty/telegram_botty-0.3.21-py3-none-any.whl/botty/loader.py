from botty_core import App, Texts, env

BOT_TOKEN = env.get("BOT_TOKEN")
STORAGE_PATH = env.get("STORAGE_PATH")
TEXTS_PATH = env.get("TEXTS_PATH")

app = App(BOT_TOKEN, STORAGE_PATH)
texts = Texts(TEXTS_PATH)
