'''
Async version

[ Air Alert Module V 1.0.0 ]

Made with love by Romikan from Kyiv, Ukraine

MIT License
'''
# Importing libraries

import io
import aiohttp
import asyncio
import requests
from PIL import Image

# Defining AlertClass

class AsyncAlertClass:

    # Defining alerts dictionary function

    async def get_alerts(self):
        # Alerts dictionary
        alerts = {
            "kyiv": False,
            "chernivtsi_region": False,
            "ivano-frankivsk_region": False,
            "volyn_region": False,
            "zakarpattia_region": False,
            "zaporizhia_region": False,
            "zhytomyr_region": False,
            "kirovohrad_region": False,
            "kyiv_region": False,
            "luhansk_region": False,
            "lviv_region": False,
            "mykolaiv_region": False,
            "odesa_region": False,
            "poltava_region": False,
            "rivne_region": False,
            "sumy_region": False,
            "ternopil_region": False,
            "kharkiv_region": False,
            "kherson_region": False,
            "khmelnytskyi_region": False,
            "chernihiv_region": False,
            "cherkasy_region" : False,
            "donetsk_region" : False,
            "vinnytsia_region" : False,
            "dnipropetrovsk_region" : False
        }

        # Getting the map image before finding colors on it
        async with aiohttp.ClientSession() as session:
            async with session.get('https://alerts.com.ua/map.png') as resp:
                if resp.status != 200:
                    raise Exception("Unable to download image (Response status code 200)")
            data = io.BytesIO(await resp.read())

        # Opening image
        img = Image.open(data)

        # Cities and their position on image
        kvcity = img.getpixel((461, 173))
        lh = img.getpixel((944, 272))
        kh = img.getpixel((777, 211))
        khr = img.getpixel((670, 461))
        od = img.getpixel((442, 442))

        lv = img.getpixel((124,212))
        kv = img.getpixel((440,220))
        ch = img.getpixel((520,100))
        zh = img.getpixel((350,125))
        zp = img.getpixel((755, 410))
        pl = img.getpixel((646,226))
        zk = img.getpixel((44, 344))
        sm = img.getpixel((647,107))
        rv = img.getpixel((240,81))
        mv = img.getpixel((590,409))
        kv = img.getpixel((560,340))
        khm = img.getpixel((281,231))
        tn = img.getpixel((200,240))
        chk = img.getpixel((540,260))
        vnt = img.getpixel((300,325))
        vln = img.getpixel((170,120))
        dnt = img.getpixel((865,417))
        chrn = img.getpixel((220,360))
        dnpt = img.getpixel((684,337))
        iv = img.getpixel((138,320))

        # Getting the color. If red color finded changing status of region to True (Alert)

        if not kvcity == (119, 170, 85, 255):
            alerts['kyiv'] = True
        if not lh == (119, 170, 85, 255):
            alerts['luhansk_region'] = True
        if not kh == (119, 170, 85, 255):
            alerts['kharkiv_region'] = True
        if not khr == (119, 170, 85, 255):
            alerts['kherson_region'] = True
        if not od == (119, 170, 85, 255):
            alerts['odesa_region'] = True
        if not lv == (119, 170, 85, 255):
            alerts['lviv_region'] = True
        if not kv == (119, 170, 85, 255):
            alerts['kyiv_region'] = True
        if not ch == (119, 170, 85, 255):
            alerts['chernihiv_region'] = True
        if not zh == (119, 170, 85, 255):
            alerts['zhytomyr_region'] = True
        if not zp == (119, 170, 85, 255):
            alerts['zaporizhia_region'] = True
        if not pl == (119, 170, 85, 255):
            alerts['poltava_region'] = True
        if not zk == (119, 170, 85, 255):
            alerts['zakarpattia_region'] = True
        if not sm == (119, 170, 85, 255):
            alerts['sumy_region'] = True
        if not rv == (119, 170, 85, 255):
            alerts['rivne_region'] = True
        if not mv == (119, 170, 85, 255):
            alerts['mykolaiv_region'] = True
        if not kv == (119, 170, 85, 255):
            alerts['kirovohrad_region'] = True
        if not iv == (119, 170, 85, 255):
            alerts['ivano-frankivsk_region'] = True
        if not khm == (119, 170, 85, 255):
            alerts['khmelnytskyi_region'] = True
        if not tn == (119, 170, 85, 255):
            alerts['ternopil_region'] = True
        if not chk == (119, 170, 85, 255):
            alerts['cherkasy_region'] = True
        if not vnt == (119, 170, 85, 255):
            alerts['vinnytsia_region'] = True
        if not vln == (119, 170, 85, 255):
            alerts['volyn_region'] = True
        if not dnt == (119, 170, 85, 255):
            alerts['donetsk_region'] = True
        if not chrn == (119, 170, 85, 255):
            alerts['chernivtsi_region'] = True
        if not dnpt == (119, 170, 85, 255):
            alerts['dnipropetrovsk_region'] = True

        # Returning list of alerts

        return alerts

    # Defining function for getting list of alerts

    def alerts_list(self):

        # Importing needed libraries

        import io
        import aiohttp
        from PIL import Image

        # Geting image of a map

        async with aiohttp.ClientSession() as session:
            async with session.get('https://alerts.com.ua/map.png') as resp:
                if resp.status != 200:
                    raise Exception("Unable to download image (Response status code 200)")
                data = io.BytesIO(await resp.read())
        
        # Opening image, defining empty list and defining coordinates of each region
        img = Image.open(data)
        tryvogi = []
        kvcity = img.getpixel((461, 173))
        lh = img.getpixel((944, 272))
        kh = img.getpixel((777,211))
        khr = img.getpixel((670, 461))
        od = img.getpixel((442,442))
        lv = img.getpixel((124,212))
        kv = img.getpixel((437,224))
        ch = img.getpixel((520,100))
        zh = img.getpixel((350,125))
        zp = img.getpixel((755, 410))
        pl = img.getpixel((646,226))
        zk = img.getpixel((44, 344))
        sm = img.getpixel((647,107))
        rv = img.getpixel((240,81))
        mv = img.getpixel((590,409))
        kv = img.getpixel((560,340))
        khm = img.getpixel((281,231))
        tn = img.getpixel((200,240))
        chk = img.getpixel((540,260))
        vnt = img.getpixel((300,325))
        vln = img.getpixel((170,120))
        dnt = img.getpixel((865,417))
        chrn = img.getpixel((220,360))
        dnpt = img.getpixel((684,337))
        iv = img.getpixel((138,320))

        # Checking if region is red
        if not kvcity == (119, 170, 85, 255):
            tryvogi.append('kyiv')
        if not lh == (119, 170, 85, 255):
            tryvogi.append('luhansk_region')
        if not kh == (119, 170, 85, 255):
            tryvogi.append('kharkiv_region')
        if not khr == (119, 170, 85, 255):
            tryvogi.append('kherson_region')
        if not od == (119, 170, 85, 255):
            tryvogi.append('odesa_region')
        if not lv == (119, 170, 85, 255):
            tryvogi.append('lviv_region')
        if not kv == (119, 170, 85, 255):
            tryvogi.append('kyiv_region')
        if not ch == (119, 170, 85, 255):
            tryvogi.append('chernihiv_region')
        if not zh == (119, 170, 85, 255):
            tryvogi.append('zhytomyr_region')
        if not zp == (119, 170, 85, 255):
            tryvogi.append('zaporizhia_region')
        if not pl == (119, 170, 85, 255):
            tryvogi.append('poltava_region')
        if not zk == (119, 170, 85, 255):
            tryvogi.append('zakarpattia_region')
        if not sm == (119, 170, 85, 255):
            tryvogi.append('sumy_region')
        if not rv == (119, 170, 85, 255):
            tryvogi.append('rivne_region')
        if not mv == (119, 170, 85, 255):
            tryvogi.append('mykolaiv_region')
        if not kv == (119, 170, 85, 255):
            tryvogi.append('kirovohrad_region')
        if not iv == (119, 170, 85, 255):
            tryvogi.append('ivano-frankivsk_region')
        if not khm == (119, 170, 85, 255):
            tryvogi.append('khmelnytskyi_region')
        if not tn == (119, 170, 85, 255):
            tryvogi.append('ternopil_region')
        if not chk == (119, 170, 85, 255):
            tryvogi.append('cherkasy_region')
        if not vnt == (119, 170, 85, 255):
            tryvogi.append('vinnytsia_region')
        if not vln == (119, 170, 85, 255):
            tryvogi.append('volyn_region')
        if not dnt == (119, 170, 85, 255):
            tryvogi.append('donetsk_region')
        if not chrn == (119, 170, 85, 255):
            tryvogi.append('chernivtsi_region')
        if not dnpt == (119, 170, 85, 255):
            tryvogi.append('dnipropetrovsk_region')    
        
        # Returning result
        
        return tryvogi
__all__ = ['AlertClass']