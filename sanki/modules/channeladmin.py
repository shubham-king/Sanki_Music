from asyncio.queues import QueueEmpty

from pyrogram import Client, filters
from pyrogram.types import Message

from Sanki_Music.function.admins import set
from Sanki_Music.services.callsmusic import callsmusic


@Client.on_message(
    filters.command(["channelpause", "cpause"]) & filters.group & ~filters.edited
)
async def pause(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**𝐈𝐬 𝐭𝐡𝐞 𝐜𝐡𝐚𝐭 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝?**")
        return
    chat_id = chid
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❗ **𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐢𝐬 𝐏𝐥𝐚𝐲𝐢𝐧𝐠!**")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("▶️ **𝐏𝐚𝐮𝐬𝐞𝐝!**")


@Client.on_message(
    filters.command(["channelresume", "cresume"]) & filters.group & ~filters.edited
)
async def resume(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**𝐈𝐬 𝐭𝐡𝐞 𝐂𝐡𝐚𝐭 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝?**")
        return
    chat_id = chid
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❗ **𝐍𝐨𝐓𝐡𝐢𝐧𝐠 𝐢𝐬 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 𝐂𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("⏸ **𝐑𝐞𝐬𝐮𝐦𝐞𝐝!**")


@Client.on_message(
    filters.command(["channelend", "cend"]) & filters.group & ~filters.edited
)
async def stop(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**𝐈𝐬 𝐭𝐡𝐞 𝐜𝐡𝐚𝐭 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝?**")
        return
    chat_id = chid
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ **𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐢𝐬 𝐂𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲 𝐏𝐥𝐚𝐲𝐢𝐧𝐠!**")
    else:
        try:
            callsmusic.queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("❌ **𝐒𝐭𝐨𝐩𝐩𝐢𝐧𝐠 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠!**")


@Client.on_message(
    filters.command(["channelskip", "cskip"]) & filters.group & ~filters.edited
)
async def skip(_, message: Message):
    global que
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**𝐈𝐬 𝐭𝐡𝐞 𝐂𝐡𝐚𝐭 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝?**")
        return
    chat_id = chid
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ **𝐓𝐡𝐞𝐫𝐞 𝐢𝐬 𝐍𝐨 𝐧𝐞𝐱𝐭 𝐒𝐨𝐧𝐠 𝐭𝐨 𝐒𝐤𝐢𝐩😑!**")
    else:
        callsmusic.queues.task_done(chat_id)

        if callsmusic.queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, callsmusic.queues.get(chat_id)["file"]
            )

        await message.reply_text("⏩ **𝐒𝐤𝐢𝐩𝐩𝐞𝐝 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐒𝐨𝐧𝐠!**")


@Client.on_message(filters.command("channeladmincache"))
async def admincache(client, message: Message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**𝐈𝐬 𝐭𝐡𝐞 𝐜𝐡𝐚𝐭 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝?**")
        return
    set(
        chid,
        [
            member.user
            for member in await conchat.linked_chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("✅️ **𝐀𝐝𝐦𝐢𝐧 𝐥𝐢𝐬𝐭** 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 **𝐮𝐩𝐝𝐚𝐭𝐞𝐝**")
