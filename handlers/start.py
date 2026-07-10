from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

def main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    
    # Hero Button
    markup.row(InlineKeyboardButton("⟡ 𝗜𝗡𝗜𝗧𝗜𝗔𝗧𝗘 𝗗𝗘𝗣𝗟𝗢𝗬𝗠𝗘𝗡𝗧 ⟡", callback_data="menu_create_list"))
    
    # Control Panel Buttons
    markup.add(
        InlineKeyboardButton("⎔ Access Control", callback_data="menu_akses"),
        InlineKeyboardButton("⎔ Owner Console", callback_data="menu_owner")
    )
    
    # Utility Buttons
    markup.add(
        InlineKeyboardButton("◈ User Identity", callback_data="btn_cekid"),
        InlineKeyboardButton("🌐 Cloud Panel", url=config.DOMAIN)
    )
    return markup

def get_main_text(user_name, user_id):
    return (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"     ❖ *{config.BOT_NAME} 𝗖𝗟𝗢𝗨𝗗* ❖\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Welcome to the Automated Deployment Matrix.\n"
        "Secure, Lightning-Fast, and Highly Optimized.\n\n"
        "⌬ *𝗦𝗬𝗦𝗧𝗘𝗠 𝗢𝗩𝗘𝗥𝗩𝗜𝗘𝗪*\n"
        "├ 📡 Core Network ⪼ `Connected`\n"
        "├ 🛡️ Ptero API    ⪼ `Authorized`\n"
        "└ ⚡ Latency      ⪼ `12ms`\n\n"
        "⌬ *𝗦𝗘𝗦𝗦𝗜𝗢𝗡 𝗜𝗡𝗙𝗢*\n"
        f"├ 👤 Operator ⪼ `{user_name}`\n"
        f"└ 🔑 Auth ID  ⪼ `{user_id}`\n\n"
        "⪼ _Awaiting initialization command..._"
    )

def register(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        text = get_main_text(message.from_user.first_name, message.from_user.id)
        bot.reply_to(message, text, reply_markup=main_menu_markup(), parse_mode="Markdown")

    @bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
    def back_to_main(call):
        text = get_main_text(call.from_user.first_name, call.from_user.id)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=main_menu_markup(), parse_mode="Markdown")
