from asyncio.queues import QueueEmpty

from pyrogram import Client, filters
from pyrogram.types import Message

from Sanki_Music.config import BOT_USERNAME
from Sanki_Music.function.admins import set
from Sanki_Music.helpers.channelmusic import get_chat_id
from Sanki_Music.helpers.decorators import authorized_users_only
from Sanki_Music.helpers.filters import command, other_filters
from Sanki_Music.services.callsmusic import callsmusic


@Client.on_message(filters.command(["adminreset", f"adminreset@{BOT_USERNAME}"]))
@authorized_users_only
async def update_admin(client, message: Message):
    chat_id = get_chat_id(message.chat)
    set(
        chat_id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("✅️ Admin cache refreshed!")


@Client.on_message(command(["pause", f"pause@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❗ **𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐈𝐬 𝐏𝐥𝐚𝐲𝐢𝐧𝐠😑!**")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("▶️ **𝙋𝙖𝙪𝙨𝙚𝙙 !**")


@Client.on_message(command(["resume", f"resume@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❗ **𝐂𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲 𝐍𝐨 𝐬𝐨𝐧𝐠 𝐢𝐬 𝐩𝐚𝐮𝐬𝐞𝐝!**")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("⏸ **𝙍𝙚𝙨𝙪𝙢𝙚!**")


@Client.on_message(command(["end", f"end@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ **𝐍𝐨𝐧𝐞 𝐒𝐨𝐧𝐠 𝐢𝐬 𝐏𝐥𝐚𝐲𝐢𝐧𝐠!**")
    else:
        try:
            callsmusic.queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("❌ **𝐒𝐭𝐨𝐩𝐩𝐢𝐧𝐠 𝐓𝐡𝐞 𝐬𝐨𝐧𝐠.!**")


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ **𝐍𝐨 𝐧𝐞𝐱𝐭 𝐒𝐨𝐧𝐠 𝐭𝐨 𝐒𝐤𝐢𝐩**")
    else:
        callsmusic.queues.task_done(chat_id)

        if callsmusic.queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, callsmusic.queues.get(chat_id)["file"]
            )

        await message.reply_text("⏩ **𝐒𝐤𝐢𝐩𝐩𝐞𝐝 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐒𝐨𝐧𝐠!**")


@Client.on_message(filters.command(["admincache", f"admincache@{BOT_USERNAME}"]))
@authorized_users_only
async def admincache(client, message: Message):
    set(
        message.chat.id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("✅️ **𝐀𝐝𝐦𝐢𝐧 𝐥𝐢𝐬𝐭** 𝐡𝐚𝐬 **𝐔𝐩𝐝𝐚𝐭𝐞𝐝**")
