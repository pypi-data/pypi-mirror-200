from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = """
👋 Hello {} Sir,
❤️ Welcome to {} ♥️
You can use me to generate pyrogram and telethon string session. Use the 👇 Below buttons to know more!
    """

    # Home Button
    home_buttons = [
        [
            InlineKeyboardButton(
                "♥️ Start Generating Session ♥️", callback_data="generate"
            )
        ],
        [InlineKeyboardButton(text="🔙 Back ", callback_data="home")],
    ]

    generate_button = [
        [InlineKeyboardButton("⚡ Start Generating Session ⚡", callback_data="generate")]
    ]

    support_button = [
        [InlineKeyboardButton("⚜ Support ⚜", url="https://t.me/TeamLegendXD")]
    ]

    # Rest Buttons
    buttons = [
        [
            InlineKeyboardButton(
                "⚡ Start Generating Session ⚡", callback_data="generate"
            )
        ],
        [
            InlineKeyboardButton(
                "📝 Repo ", url="https://github.com/LEGEND-AI/STRING-GENERATE"
            )
        ],
        [
            InlineKeyboardButton("How to Use Me❔", callback_data="help"),
            InlineKeyboardButton("🤔 About", callback_data="about"),
        ],
        [InlineKeyboardButton("Owner 🇮🇳", url="https://t.me/LegendBot_Owner")],
    ]

    # Help Message
    HELP = """
» Click the below button or use /generate command to start generating session!
» Click the required button; [Pyrogram v1/Pyrogram v2/Telethon]
» Enter the required variables when asked.
"""


     #about message
    ABOUT = """
👨‍💻 **About Me**
This is a telegram bot Help You To Generate Pyrogram V1/V2 and Telethon String Session....
[Pyrogram](docs.pyrogram.org)
[Telethon](docs.telethon.org)
Language : [Python](www.python.org)

               **Regarding ~ **@TeamLegendXD
"""
