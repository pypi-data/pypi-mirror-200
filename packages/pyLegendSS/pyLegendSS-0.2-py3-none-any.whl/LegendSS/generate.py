from .Data import Data
from pyrogram import Client, filters
from pyrogram1 import Client as Client1
from telethon.sync import TelegramClient
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telethon.tl.functions.channels import (
    JoinChannelRequest, LeaveChannelRequest)
from pyrogram.errors import (
    ApiIdInvalid, PhoneCodeExpired, PhoneCodeInvalid, PhoneNumberInvalid,
    PasswordHashInvalid, SessionPasswordNeeded)
from telethon.errors import (
    ApiIdInvalidError, PhoneCodeExpiredError, PhoneCodeInvalidError,
    PhoneNumberInvalidError, PasswordHashInvalidError,
    SessionPasswordNeededError)
from pyrogram1.errors import (
    ApiIdInvalid as ApiIdInvalid1, PhoneCodeExpired as PhoneCodeExpired1,
    PhoneCodeInvalid as PhoneCodeInvalid1,
    PhoneNumberInvalid as PhoneNumberInvalid1,
    PasswordHashInvalid as PasswordHashInvalid1,
    SessionPasswordNeeded as SessionPasswordNeeded1)

ERROR_MESSAGE = "{}\n\nSomething Error in Session Generator Bot\nReport it To @LegendBot_Owner\n          ©@TeamLegendXD"


async def generate_session(
    bot: Client, msg: Message, telethon=False, old_pyro: bool = False
):
    if telethon:
        ty = "Telethon"
    else:
        ty = "Pyrogram"
        if not old_pyro:
            ty += " ᴠ2"
    await msg.reply(f"🛡 Starting {ty} String Session Generation 🛡")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(
        user_id,
        "Please send your `API_ID`\n\nClick /skip for leave `APP_ID` & `API_HASH`.",
        filters=filters.text,
    )
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = 13519785
        api_hash = "22a8c34e40082b2fce539266efa1f531"
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply(
                "Not a valid API_ID (which must be an integer). Please start generating session again.",
                quote=True,
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        api_hash_msg = await bot.ask(
            user_id, "Please send your `API_HASH`", filters=filters.text
        )
        if await cancelled(api_id_msg):
            return
        api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(
        user_id,
        "Now please send your `PHONE_NUMBER` along with the country code. \nExample : `+917936482542`",
        filters=filters.text,
    )
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("Sending OTP...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply(
            "`API_ID` and `API_HASH` combination is invalid. Please start generating session again.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply(
            "`PHONE_NUMBER` is invalid. Please start generating session again.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    try:
        phone_code_msg = await bot.ask(
            user_id,
            "Please check for an OTP in official telegram account. If you got it, send OTP here after reading the below format. \nIf OTP is in the form ~ `12345`, **please send it as** `1 2 3 4 5`.",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply(
            "Time limit reached of 10 minutes. Please start generating session again.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply(
            "OTP is invalid. Please start generating session again.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply(
            "OTP is expired. Please start generating session again.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(
                user_id,
                "Your account has enabled two-step verification. Please provide the password.",
                filters=filters.text,
                timeout=300,
            )
        except TimeoutError:
            await msg.reply(
                "Time limit reached of 5 minutes. Please start generating session again.",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply(
                "Invalid Password Provided. Please start generating session again.",
                quote=True,
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
    if telethon:
        string_session = client.session.save()
        try:
            await client.send_message(
                "me",
                "**{} - STRING SESSION** \n\n`{}`\n\n• __Dont Share String Session With Anyone__\n• __Dont Invite Anyone To Heroku__".format(
                    "TELETHON" if telethon else "PYROGRAM", string_session
                ),
            )
        except KeyError:
            pass
        try:
            await client(JoinChannelRequest("@LegendBot_AI"))
        except BaseException:
            pass
    else:
        string_session = await client.export_session_string()
        try:
            await client.send_message(
                "me",
                "**{} ~ STRING SESSION** \n\n`{}` \n\n• __Dont Share String Session With Anyone__\n• __Dont Invite Anyone To Heroku__".format(
                    "TELETHON" if telethon else "PYROGRAM", string_session
                ),
            )
        except KeyError:
            pass
    await client.disconnect()
    await phone_code_msg.reply(
        "Successfully String  Session Has Been Generated {} \n\nPlease check your saved messages!".format(
            "TELETHON" if telethon else "PYROGRAM"
        ),
        reply_markup=InlineKeyboardMarkup(Data.support_button),
    )


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply(
            "Cancelled the Process!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif "/restart" in msg.text:
        await msg.reply(
            "Restarted the Bot!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("Cancelled the generation process!", quote=True)
        return True
    else:
        return False
