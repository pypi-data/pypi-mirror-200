from api import *

async def s_handler(client, query, chatid):
    settings = await get_settings(chatid)
    SHORTNER = settings['shortner_url']
    API = settings['shortner_api']

    resp = requests.get(f'https://{SHORTNER}/api?api={API}&url={SHORT_URL}').json()
    if resp['status'] == 'success':
        SHORT_URL = resp['shortenedUrl']
        return SHORT_URL


async def link_handler(client, query, chatid):
    settings = await get_settings(chatid)
    LINK = settings['video_link']
    return LINK
