import telegram
import requests
from model import image
from datetime import datetime
from config_reader import get_config

config = get_config()
BOT = telegram.Bot(token=config['telegram']['bot_token'])

async def send_images(images_to_notify: list[image.Image]):
    print("Sending operation started")
    await send_telegram_messages(images_to_notify)
    print("Sending operation finished")    

async def send_telegram_messages(images_to_notify):
    for image_to_send in images_to_notify:
        text_message = prepare_text_message(image_to_send)
        # Telegram can't retrieve the image directly from the CivitAi URL for some reason, so we download it first
        image_bytes = download_image(image_to_send.url) 
        await send_single_message(image_to_send, text_message, image_bytes)
        
def prepare_text_message(image: image.Image):
    return (
        f"<b>{image.username}</b>\n\n"
        f"🗓️ {format_date(image.createdAt)}\n\n"
        f"📐 {image.size}\n\n"
        f"🧠 <b>{image.model}</b>\n\n"
        f"✨ <b>Prompt:</b>\n\n{replace_tag_sign_with_square_brackets(image.prompt)}\n\n"
        f"🚫 <b>Negative:</b>\n\n{image.negativePrompt}"
    )

def replace_tag_sign_with_square_brackets(text: str):
    return text.replace('<', '[').replace('>', ']')

def format_date(stringDate: str):
    date = datetime.strptime(stringDate, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date.strftime('%B %d, %Y %H:%M') #e.g. November 28, 2023 15:45

async def send_single_message(image: image.Image, text_message, image_bytes):
    bot = get_bot()
    try:
        await bot.send_photo(
            chat_id=config['telegram']['chat_id'],
            photo=image_bytes,  # Send the actual image data
            caption=text_message,
            parse_mode=telegram.constants.ParseMode.HTML
        )
        print(f"Message correctly sent for image {image.id}")
    except Exception as e:
        print(f"Error sending message for image {image.id}: {e}")

def get_bot():
    bot = BOT
    if not bot:
        bot = telegram.Bot(token=config['telegram']['bot_token'])
    return bot

def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download image: Status code {response.status_code}")