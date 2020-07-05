from db_record.DBRecord import DBRecord
from csvupload.models import db, SiteIdPriceStartTimeNameDescriptionNickname
from typing import Iterable, List, Tuple, Dict
import requests
import asyncio
import aiohttp


class SiteIdPriceStartTimeNameDescriptionNicknameRecord(DBRecord):
    def __init__(self, file_record):
        self.site = file_record.values[0]
        self.id = file_record.values[1]
        self.price = ""
        self.start_time = ""
        self.name = ""
        self.description = ""
        self.nickname = ""
        super(SiteIdPriceStartTimeNameDescriptionNicknameRecord, self).__init__(file_record)

    def transform(self) -> bool:
        if not (self._transform_id() and self._transform_site()):
            return False

        item_request = requests.get("https://api.mercadolibre.com/items?ids=" + self.file_record.render())
        if item_request.status_code != 200:
            return False

        item = item_request.json()[0]
        if 'price' not in item['body'].keys():
            return False
        self.price = float(item['body']['price'])
        self.start_time = item['body']['start_time']

        currency_url = "https://api.mercadolibre.com/currencies/" + item['body']['currency_id']
        category_url = "https://api.mercadolibre.com/categories/" + item['body']['category_id']
        user_url = "https://api.mercadolibre.com/users/" + str(item['body']['seller_id'])

        async_request = asyncio.run(request_aio([currency_url, category_url, user_url]))

        self.description = async_request[currency_url]['description']
        self.name = async_request[category_url]['name']
        self.nickname = async_request[user_url]['nickname']

        return True

    def _transform_site(self) -> bool:
        if self.site not in ['MLB', 'MLA']:
            return False
        return True

    def _transform_id(self) -> bool:
        try:
            self.id = int(self.id)
        except ValueError:
            return False
        return True

    def save(self):
        new_record = SiteIdPriceStartTimeNameDescriptionNickname(
            site=self.site,
            item_id=self.id,
            price=self.price,
            start_time=self.start_time,
            name=self.name,
            description=self.description,
            nickname=self.nickname
        )
        db.session.add(new_record)
        db.session.commit()


async def request_aio(urls: Iterable[str]) -> Dict:
    results = {}

    async def request(url: str) -> None:
        async with aiohttp.ClientSession() as s:
            resp = await s.get(url)
            out = await resp.json()
            results[url] = out

    await asyncio.gather(*[request(url) for url in urls])
    return results
