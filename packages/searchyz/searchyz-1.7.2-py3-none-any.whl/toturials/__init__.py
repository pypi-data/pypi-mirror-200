from api import *

async def set_toturials_cmd(c, m):
    sts = await m.reply("Checking Group")
    userid = m.from_user.id if m.from_user else None
    if not userid:
        return await m.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = m.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await m.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await m.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = m.chat.id
        title = m.chat.title

    else:
        return

    st = await c.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        await m.reply_text("You Are Not Admin Of This Group", quote=True)
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to add shortner and api.\n\nUsage: `/set_tutorials {DEFULT_VIDEO_LINK}`\n\nIf Your CHannel is Private Then Bot Make Request Link",
            quote=True,
        )
        return

    try:
        DK = m.command[1]
        await save_group_settings(grp_id, 'video_link', DK)
        await m.reply_text(f"Your VIDEO is Added\n\nNow You Can See Your Video Link\n\nYour Video Link : {m.text}", quote=True)

    except Exception as e:
        await save_group_settings(grp_id, 'video_link', DEFULT_VIDEO_LINK)
        await m.reply_text(
            f"Error occoured!! {e}\n\nAuto Defult Video Link Added\n\nYou Can Also Contact Our Support Group For Solve This issue\n\nFormat - `/set_tutorials {DEFULT_VIDEO_LINK}`",
            quote=True,
        )