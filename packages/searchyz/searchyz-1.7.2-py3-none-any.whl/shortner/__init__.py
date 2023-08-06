from api import *

async def set_shortner_cmd(c, m):
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
            "Use this command to add shortner and api.\n\nUsage:\n\n`/set_shortner mdiskpro.xyz cbd63775f798fe0e58c67a56e6ce8b70c495cda4` ",
            quote=True,
        )
        return

    try:
        URL = m.command[1]
        API = m.command[2]
        resp = requests.get(f'https://{URL}/api?api={API}&url=https://t.me/DKBOTZ').json()
        if resp['status'] == 'success':
            SHORT_LINK = resp['shortenedUrl']
        await save_group_settings(grp_id, 'shortner_url', URL)
        await save_group_settings(grp_id, 'shortner_api', API)
        await m.reply_text(f"Your Site is Added\n\nNow You Can See Your Shorted Link\n\nDemo : {SHORT_LINK}\n\nShortner Site : {URL}\n\nAPI : {API}", quote=True)

    except Exception as e:
        await save_group_settings(grp_id, 'shortner_url', DEFULT_SHORTNER_URL)
        await save_group_settings(grp_id, 'shortner_api', DEFULT_SHORTNER_API)
        await m.reply_text(
            f"Error occoured!! {e}\n\nAuto Added Defult Shortner\n\nIf You Want Change Then Use Correct Format And Valid Shortner Website\n\nYou Can Also Contact Our Support Group For Solve This issue\n\nFormat - `/set_shortner mdiskpro.xyz cbd63775f798fe0e58c67a56e6ce8b70c495cda4`",
            quote=True,
        )
