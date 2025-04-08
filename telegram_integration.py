import telegram
import requests
from model import image
from datetime import datetime
from config_reader import get_config
from typing import List # Retrocompatibility with older versions of Python (Raspberry Pi 3.7)
from logger_config import logger

config = get_config()
BOT = telegram.Bot(token=config['telegram']['bot_token'])

async def send_images(images_to_notify: List[image.Image]):
    logger.info("Sending operation started")
    await send_telegram_messages(images_to_notify)
    logger.info("Sending operation finished")

async def send_telegram_messages(images_to_notify):
    for image_to_send in images_to_notify:

        # Split image data and prompt because Telegram has a limit of characters
        image_caption = prepare_caption_message(image_to_send)
        text_message = prepare_text_message(image_to_send)

        # Telegram can't retrieve the image directly from the CivitAi API URL for some reason, so we download it first
        image_bytes = download_image(image_to_send.url) 

        await send_single_message(image_to_send, image_caption, text_message, image_bytes)
        
def prepare_caption_message(image: image.Image):
    return (
        f"<b>{image.username}</b>\n\n"
        f"🗓️ {format_date(image.createdAt)}\n\n"
        f"🔗 https://civitai.com/images/{image.id}\n\n"
    )

def prepare_text_message(image: image.Image):
    return (
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

async def send_single_message(image: image.Image, image_caption, text_message, image_bytes):
    bot = get_bot()
    caption_limit = telegram.constants.MessageLimit.CAPTION_LENGTH
    text_message_limit = telegram.constants.MessageLimit.MAX_TEXT_LENGTH
    try:
        await bot.send_photo(
            chat_id=config['telegram']['chat_id'],
            photo=image_bytes,  # Send the actual image data
            caption=image_caption if len(image_caption) < caption_limit else image_caption[:caption_limit-3] + "...", # Truncate if over telegram limits
            parse_mode=telegram.constants.ParseMode.HTML
        )

        await bot.send_message(
            chat_id=config['telegram']['chat_id'],
            text=text_message if len(text_message) < text_message_limit else text_message[:text_message_limit-3] + "...", # Truncate if over telegram limits
            parse_mode=telegram.constants.ParseMode.HTML
        )

        logger.info(f"Message correctly sent for image {image.id}")
    except Exception as e:
        logger.error(f"Error sending message for image {image.id}: {e}")

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