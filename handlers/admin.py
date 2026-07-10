from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from database import load_db, save_db, is_owner

def register(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ["menu_akses", "menu_owner"])
    def admin_menus(call):
        if not is_owner(call.from_user.id):
            return bot.answer_callback_query(call.id, "✖ PERMISSION DENIED", show_alert=True)
            
        markup = InlineKeyboardMarkup(row_width=2)
        if call.data == "menu_akses":
            markup.add(
                InlineKeyboardButton("⟡ Grant Access", callback_data="action_addakses"),
                InlineKeyboardButton("⨯ Revoke Access", callback_data="action_delakses")
            )
            markup.row(InlineKeyboardButton("◈ View Access Matrix", callback_data="action_listakses"))
            title = "𝗔𝗖𝗖𝗘𝗦𝗦 𝗖𝗢𝗡𝗧𝗥𝗢𝗟 𝗠𝗔𝗧𝗥𝗜𝗫"
        else:
            markup.add(
                InlineKeyboardButton("⟡ Grant Owner", callback_data="action_addowner"),
                InlineKeyboardButton("⨯ Revoke Owner", callback_data="action_delowner")
            )
            markup.row(InlineKeyboardButton("◈ View Owner Matrix", callback_data="action_listowner"))
            title = "𝗢𝗪𝗡𝗘𝗥 𝗖𝗢𝗡𝗧𝗥𝗢𝗟 𝗠𝗔𝗧𝗥𝗜𝗫"
            
        markup.row(InlineKeyboardButton("⪡ RETURN TO CORE", callback_data="back_to_main"))
        
        text = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   🛡️ *{title}* 🛡️\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⪼ _Warning: Authorized modifications only._\n"
            "⪼ _Select execution protocol:_"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("action_"))
    def handle_admin_actions(call):
        if not is_owner(call.from_user.id):
            return bot.answer_callback_query(call.id, "✖ DENIED", show_alert=True)

        action = call.data.split("_")[1]
        db = load_db()

        if action in ["listakses", "listowner"]:
            target_list = db["akses"] if action == "listakses" else db["owners"]
            
            if not target_list:
                users_text = "Database is empty."
            else:
                users_text = "\n".join([f"UID: {uid}" for uid in target_list])
                
            judul = "ACCESS UID REGISTRY" if action == "listakses" else "OWNER UID REGISTRY"
            
            # Print using Code Block for terminal feel
            text = f"```text\n[{judul}]\n--------------------\n{users_text}\n```"
            
            bot.answer_callback_query(call.id, "Querying Database...")
            bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
            return

        text = (
            f"⌬ *[𝗣𝗥𝗢𝗧𝗢𝗖𝗢𝗟 : {action.upper()}]*\n"
            f"└ ⪼ _Enter Target Telegram ID:_"
        )
        msg = bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_admin_input, action)

    def process_admin_input(message, action):
        if message.text.startswith('/'):
            return bot.reply_to(message, "✖ 𝗔𝗕𝗢𝗥𝗧𝗘𝗗.")
            
        try:
            target_id = int(message.text)
        except:
            return bot.reply_to(message, "✖ 𝗘𝗥𝗥𝗢𝗥: Invalid ID formatting.")

        db = load_db()
        if action == "addakses":
            if target_id not in db["akses"]: db["akses"].append(target_id)
            save_db(db)
            bot.reply_to(message, f"✅ `[PROTOCOL SUCCESS]` Access granted to UID `{target_id}`.", parse_mode="Markdown")
        elif action == "delakses":
            if target_id in db["akses"]: db["akses"].remove(target_id)
            save_db(db)
            bot.reply_to(message, f"✅ `[PROTOCOL SUCCESS]` Access revoked from UID `{target_id}`.", parse_mode="Markdown")
        elif action == "addowner":
            if target_id not in db["owners"]: db["owners"].append(target_id)
            save_db(db)
            bot.reply_to(message, f"✅ `[PROTOCOL SUCCESS]` Owner status granted to UID `{target_id}`.", parse_mode="Markdown")
        elif action == "delowner":
            if target_id in db["owners"]: db["owners"].remove(target_id)
            save_db(db)
            bot.reply_to(message, f"✅ `[PROTOCOL SUCCESS]` Owner status revoked from UID `{target_id}`.", parse_mode="Markdown")
