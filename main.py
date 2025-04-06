import civitai_data_retriever as civitai
import io_handler as io
import image_comparison
import telegram_integration as telegram
import asyncio
from config_reader import get_config
from logger_config import logger

config = get_config()

async def main():
    logger.info("Starting script execution")
    for username in config['users']:

        # Fetching data from CivitAi and the last save log
        current_user_images = fetch_data(username)
        last_user_log = fetch_last_log(username)
        
        # Checking images that need to be notified
        images_to_notify = get_images_to_notify(last_user_log, current_user_images)
        if not images_to_notify:
            continue

        # Sending new images to Telegram
        await telegram.send_images(images_to_notify)
        
        # Saving new log of fetched images only when the sending process is successful
        io.save_new_log(current_user_images, username)

    logger.info("Finished script execution")

def fetch_data(username):
    logger.info(f'Fetching images for {username}')
    current_user_images = civitai.retrieve_user_images(username)
    if not current_user_images:
        raise Exception("Error: something went wrong in retrieving data from CivitAI")
    return current_user_images

def fetch_last_log(username):
    return io.get_last_saved_log(username)

def get_images_to_notify(last_user_log, current_user_images):
    if not last_user_log:
        return current_user_images
    else:
        images_to_notify = image_comparison.look_for_new_images(current_user_images, last_user_log)
        return images_to_notify

if __name__ == "__main__":
    asyncio.run(main())