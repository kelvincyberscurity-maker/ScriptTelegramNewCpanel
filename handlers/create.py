from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import is_akses
from pterodactyl import create_ptero_user, create_ptero_server
import config
import random
import string
import time # WAJIB DITAMBAHKAN UNTUK ANIMASI

ACTIVE_SESSIONS = {}

def register(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "menu_create_list")
    def show_create_menu(call):
        if not is_akses(call.from_user.id):
            return bot.answer_callback_query(call.id, "✖ UNAUTHORIZED ACTION", show_alert=True)
        
        if ACTIVE_SESSIONS.get("is_busy", False):
            return bot.answer_callback_query(call.id, "⚠ MATRIX BUSY! Another deployment is running.", show_alert=True)
            
        markup = InlineKeyboardMarkup(row_width=3)
        
        # Grid Button dengan gaya HUD
        buttons = []
        for i in range(1, 10):
            num = f"0{i}" if i < 10 else str(i)
            buttons.append(InlineKeyboardButton(f"▪ {num} GB ▪", callback_data=f"create_{i}gb"))
        markup.add(*buttons)
        
        markup.row(
            InlineKeyboardButton("▪ 10 GB ▪", callback_data="create_10gb"),
            InlineKeyboardButton("✧ MAX UNLIMITED ✧", callback_data="create_unli")
        )
        markup.row(InlineKeyboardButton("⪡ RETURN TO CORE", callback_data="back_to_main"))
        
        text = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "    ⟡ *𝗥𝗘𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗟𝗟𝗢𝗖𝗔𝗧𝗢𝗥* ⟡\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⌬ *𝗦𝗣𝗘𝗖𝗜𝗙𝗜𝗖𝗔𝗧𝗜𝗢𝗡𝗦:*\n"
            "├ ⚙️ Architecture ⪼ `Node.js V8 Engine`\n"
            "├ 🌐 Connection   ⪼ `10Gbps Uplink`\n"
            "└ 🛡️ Protection   ⪼ `L7 Anti-DDoS`\n\n"
            "⪼ _Select your desired computational power:_"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        
    @bot.callback_query_handler(func=lambda call: call.data.startswith("create_"))
    def ask_target_id(call):
        user_id = call.from_user.id
        if not is_akses(user_id):
            return bot.answer_callback_query(call.id, "✖ ACCESS DENIED", show_alert=True)
            
        if ACTIVE_SESSIONS.get("is_busy", False):
            return bot.answer_callback_query(call.id, "⚠ Engine Busy.", show_alert=True)
            
        ram_type = call.data.split("_")[1]
        bot.answer_callback_query(call.id)
        
        ACTIVE_SESSIONS["is_busy"] = True
        ACTIVE_SESSIONS["current_operator"] = user_id
        
        text = (
            f"⌬ *[𝗦𝗧𝗘𝗣 𝟭/𝟮] 𝗧𝗔𝗥𝗚𝗘𝗧 𝗜𝗗𝗘𝗡𝗧𝗜𝗙𝗜𝗖𝗔𝗧𝗜𝗢𝗡*\n"
            f"├ 📦 Selected ⪼ `{ram_type.upper()}`\n"
            f"└ ⪼ _Input Target Telegram ID:_"
        )
        msg = bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(msg, ask_username, ram_type)

    def ask_username(message, ram_type):
        user_id = message.from_user.id
        if user_id != ACTIVE_SESSIONS.get("current_operator"): return
            
        if message.text.startswith('/'):
            ACTIVE_SESSIONS["is_busy"] = False
            return bot.reply_to(message, "✖ 𝗔𝗕𝗢𝗥𝗧𝗘𝗗: Process terminated.")
            
        target_id = message.text
        if not target_id.isdigit():
            ACTIVE_SESSIONS["is_busy"] = False
            return bot.reply_to(message, "✖ 𝗘𝗥𝗥𝗢𝗥: ID must be numeric! Aborted.")

        text = (
            f"⌬ *[𝗦𝗧𝗘𝗣 𝟮/𝟮] 𝗦𝗘𝗥𝗩𝗘𝗥 𝗜𝗗𝗘𝗡𝗧𝗜𝗧𝗬*\n"
            f"├ 📦 Selected ⪼ `{ram_type.upper()}`\n"
            f"├ 🎯 Target ID ⪼ `{target_id}`\n"
            f"└ ⪼ _Input Server Username (No Spaces):_"
        )
        msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_deployment, ram_type, target_id)

    def process_deployment(message, ram_type, target_id):
        user_id = message.from_user.id
        if user_id != ACTIVE_SESSIONS.get("current_operator"): return

        if message.text.startswith('/'):
            ACTIVE_SESSIONS["is_busy"] = False
            return bot.reply_to(message, "✖ 𝗔𝗕𝗢𝗥𝗧𝗘𝗗: Sequence broken.")
            
        username = message.text.replace(" ", "")
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        email = f"{username}@vinzcloud.net"

        if ram_type == "unli":
            ram_mb = 0; cpu = 0; disk = 0
        else:
            gb = int(ram_type.replace("gb", ""))
            ram_mb = gb * 1024; cpu = gb * 100; disk = ram_mb

        # ========================================
        # EFEK ANIMASI LOADING BAR DIMULAI DI SINI
        # ========================================
        msg_wait = bot.reply_to(message, "▱▱▱▱▱▱▱▱▱▱ [0%] Initiating Sequence...")
        
        try:
            time.sleep(0.5)
            bot.edit_message_text("▰▰▱▱▱▱▱▱▱▱ [20%] Generating Cryptographic Keys...", message.chat.id, msg_wait.message_id)
            
            success_user, user_result = create_ptero_user(username, email, password)
            if not success_user:
                return bot.edit_message_text(f"✖ `[FATAL ERROR]`\nUser creation failed:\n`{user_result}`", message.chat.id, msg_wait.message_id, parse_mode="Markdown")

            time.sleep(0.5)
            bot.edit_message_text("▰▰▰▰▰▰▱▱▱▱ [60%] Allocating Hardware Resources...", message.chat.id, msg_wait.message_id)

            success_server, server_result = create_ptero_server(f"Vinz_{username}", user_result, ram_mb, disk, cpu)

            time.sleep(0.5)
            bot.edit_message_text("▰▰▰▰▰▰▰▰▰▱ [90%] Finalizing Container Network...", message.chat.id, msg_wait.message_id)
            time.sleep(0.5)

            if success_server:
                # STRUK BUKTI MENGGUNAKAN CODE BLOCK (DARK MODE)
                struk = (
                    "```text\n"
                    "===================================\n"
                    "       VINZ CLOUD DEPLOYMENT       \n"
                    "===================================\n"
                    "STATUS       : SUCCESS / ACTIVE    \n"
                    f"SERVER NODE  : ID-JKT-{ram_type.upper()}    \n"
                    "-----------------------------------\n"
                    " [ CREDENTIALS ]                   \n"
                    f" Username    : {username}          \n"
                    f" Password    : {password}          \n"
                    f" RAM Config  : {ram_type.upper()}  \n"
                    "-----------------------------------\n"
                    f" Login URL   : {config.DOMAIN}     \n"
                    "===================================\n"
                    "* IMPORTANT: Save this credential *\n"
                    "```"
                )
                
                msg_to_user = f"🎉 *𝗦𝗘𝗥𝗩𝗘𝗥 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬 𝗗𝗘𝗣𝗟𝗢𝗬𝗘𝗗* 🎉\n\n{struk}"
                
                try:
                    bot.send_message(target_id, msg_to_user, parse_mode="Markdown")
                    bot.edit_message_text(f"✅ `[DEPLOYMENT 100% COMPLETE]`\n⪼ Data securely delivered to ID `{target_id}`.", message.chat.id, msg_wait.message_id, parse_mode="Markdown")
                except Exception:
                    fallback_msg = (
                        f"✅ `[DEPLOYMENT 100% COMPLETE]`\n"
                        f"⚠ `[PM BLOCKED]` Target has not started the bot!\n\n"
                        f"⪼ *MANUAL DELIVERY REQUIRED:*\n{struk}"
                    )
                    bot.edit_message_text(fallback_msg, message.chat.id, msg_wait.message_id, parse_mode="Markdown")
            else:
                bot.edit_message_text(f"✖ `[FATAL ERROR]`\nServer allocation failed:\n`{server_result}`", message.chat.id, msg_wait.message_id, parse_mode="Markdown")
                
        finally:
            ACTIVE_SESSIONS["is_busy"] = False
            ACTIVE_SESSIONS["current_operator"] = None
