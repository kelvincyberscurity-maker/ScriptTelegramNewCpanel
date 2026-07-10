def register(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "btn_cekid")
    def action_cekid(call):
        user_id = call.from_user.id
        first_name = call.from_user.first_name
        
        # Muncul Alert Pop-up di layar
        bot.answer_callback_query(
            call.id, 
            f"👤 USER: {first_name}\n🆔 ID: {user_id}", 
            show_alert=True
        )
        
        # Kirim ID Card ke chat
        text = (
            "┌───[ 💳 𝗜𝗗𝗘𝗡𝗧𝗜𝗧𝗬 𝗖𝗔𝗥𝗗 ]\n"
            f"│ 👤 *Name* : `{first_name}`\n"
            f"│ 🆔 *Auth ID* : `{user_id}`\n"
            "└─────────────────────\n"
            "⚠️ _Use this ID to receive panel servers._"
        )
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
