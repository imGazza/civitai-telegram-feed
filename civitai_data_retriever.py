import requests
from model import image
from config_reader import get_config

config = get_config()

def retrieve_user_images(username):
    json_result = get_from_civitai(username)
    if not json_result:
        return None

    images = translate_result(json_result)
    return images

def get_from_civitai(username):
    call_headers = {
        'Autorization': f"Bearer {config['civitai']['api_token']}",
        'Content-Type': 'application/json',
    }
    params = config['civitai']['query_params']
    params.update({'username': username})
        
    response = requests.get(config['civitai']['base_url'], headers=call_headers, params=params)
    if(response.status_code == 200):
        return response.json()
    else:
        return None

def translate_result(json_result):
    images = []
    for item in json_result.get('items'):
        images.append(create_image(item))

    return images

def create_image(json_item):
    meta = json_item.get('meta', {})
    return image.Image(
        id=json_item['id'], 
        url=json_item['url'], 
        createdAt=json_item['createdAt'],
        size=meta.get('Size', 'Unknown'),
        prompt=meta.get('prompt', 'Unknown'), 
        negativePrompt=meta.get('negativePrompt', 'Unknown'), 
        username=json_item['username'], 
        model=meta.get('Model', 'Unknown'))