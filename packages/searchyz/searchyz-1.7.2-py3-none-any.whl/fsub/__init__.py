from api import *

async def force(bot, cmd, channel, group_id):
    try:
        UPDATES_CHANNEL = channel
        group = group_id
        user = await bot.get_chat_member(int(UPDATES_CHANNEL), cmd.from_user.id)
        if user.status == "kicked":
            await bot.send_message(f"Sorry Sir, You are Banned to use me. Request Admin For Unban me From Your Channel",
                disable_web_page_preview=True
            )
            return 400
    except UserNotParticipant:
        try:
            invite_link = await bot.create_chat_invite_link(int(UPDATES_CHANNEL), creates_join_request=True)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            return 400
        dkbotz = await bot.get_me()
        await cmd.reply_text(f"**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                    ]
                ]
            ),
            disable_web_page_preview=True
        )
        return 400
    except Exception:
        await cmd.reply_text(f"Something went Wrong. Contact my Support Group.\n\nThis Group Force Subscribe is Off Now\n\n@admin Again Add Fsub\n\nAlso Make Me Admin",
            disable_web_page_preview=True
        )
        await save_group_settings(group, 'fsub', False)
        return 400

async def fsub_checker(client,message, group_id):
    settings = await get_settings(group_id)
    FOR_DKBOTZ = settings['fsub']
    channel = FOR_DKBOTZ
    if FOR_DKBOTZ:
        fsub = await force(client, message, channel, group_id)
        if fsub == 400:
            return