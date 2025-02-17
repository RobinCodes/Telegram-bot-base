import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext
import requests

#IP lookup code | here for example of what you could add
async def ip_lookup(update, context):
    ip_address = context.args[0]
    url = f'http://ip-api.com/json/{ip_address}' 

    try:
        response = requests.get(url)
        data = response.json()
        
        country = data['country']
        region = data['regionName']
        city = data['city']
        zip_code = data['zip']
        timezone = data['timezone']
        isp = data['isp']
        org = data['org']
        lat = data['lat']
        lon = data['lon']
        
        message = f'```\nIP: {ip_address}\n\nCountry: {country}\nRegion: {region}\nCity: {city}\nZip Code: {zip_code}\nTimezone: {timezone}\nISP: {isp}\nOrganization: {org}\nLatitude: {lat}\nLongitude: {lon}```'
        await update.message.reply_text(message, parse_mode='MarkdownV2')
    
    except Exception as e:
        await update.message.reply_text(f'Error occurred: {str(e)}', parse_mode='MarkdownV2')

# logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# start command
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    image_url = 'https://i.postimg.cc/t4yqG1zn/image.png' # random place holder image (replace)

    keyboard = [
        [InlineKeyboardButton("🔎 IP Lookup", callback_data='IP Lookup'), InlineKeyboardButton("📞 Contact", callback_data='Contact')]
        #to add more buttons add a comma to the end of contact and start making more buttons here
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(chat_id=chat_id, parse_mode='MarkdownV2', photo=image_url, caption='👋 *Welcome to BOT NAME HERE* 👋', reply_markup=reply_markup)

async def options(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'IP Lookup':
        keyboard = [
            [InlineKeyboardButton("Back", callback_data='Back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            caption='🔒💻👁️ *Command List* 🔒💻👁️\n\n👉 IP Lookup: /lookup [IP]',
            parse_mode='MarkdownV2',
            reply_markup=reply_markup
        )

    elif query.data == 'Contact':
        keyboard = [
            [InlineKeyboardButton("Back", callback_data='Back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            caption='📞 *Contact*\n\nCONTACT DETAILS HERE',
            parse_mode='MarkdownV2',
            reply_markup=reply_markup
        )

    elif query.data == 'Back':
        keyboard = [
            [InlineKeyboardButton("🔎 IP Lookup", callback_data='IP Lookup'), InlineKeyboardButton("📞 Contact", callback_data='Contact')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            caption='👋 *Welcome to BOT NAME HERE* 👋',
            parse_mode='MarkdownV2',
            reply_markup=reply_markup
        )
    else:
        raise ValueError(f"Unsupported query data: {query.data}")

def main() -> None:
    token = "TOKEN_GOES_HERE"

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start)) # /start command
    app.add_handler(CommandHandler('lookup', ip_lookup)) # /iplookup command
    app.add_handler(CallbackQueryHandler(options))

    # Start the Bot
    app.run_polling()

if __name__ == '__main__':
    main()
