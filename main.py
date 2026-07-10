import telebot
import config
from keep_alive import keep_alive
from handlers import start, admin, create, utils

bot = telebot.TeleBot(config.BOT_TOKEN)

start.register(bot)
admin.register(bot)
create.register(bot)
utils.register(bot)

if __name__ == "__main__":
    # Menyalakan fake-server agar Pterodactyl statusnya ONLINE (Hijau)
    keep_alive() 
    print(f"🚀 {config.BOT_NAME} Sedang Berjalan di Pterodactyl Runtime...")
    bot.infinity_polling()
