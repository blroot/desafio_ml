from db_record.DBRecord import DBRecord
from csvupload.models import db, SiteIdPriceStartTimeNameDescriptionNickname
from typing import Iterable, List, Dict, Coroutine


class SiteIdPriceStartTimeNameDescriptionNicknameRecord(DBRecord):
    def __init__(self, file_record):
        self.site = file_record.values[0]
        self.id = file_record.values[1]
        self.price = ""
        self.start_time = ""
        self.name = ""
        self.description = ""
        self.nickname = ""
        self.currency_id = ""
        self.category_id = ""
        self.user_id = ""
        self.item_id = ""
        super(SiteIdPriceStartTimeNameDescriptionNicknameRecord, self).__init__(file_record)

    def retrieve_item(self, ml_api):
        item_async = ml_api.items.get(item_id=self.file_record.render())
        return True, [item_async]

    def retrieve_all_details(self, ml_api) -> (bool, List):
        if not (self._transform_id() and self._transform_site()):
            return False, []

        item = ml_api.items.get_from_cache(item_id=self.file_record.render())
        if item[0]['code'] != 200:
            return False, []

        item = item[0]
        if 'price' not in item['body'].keys():
            return False, []
        self.price = float(item['body']['price'])
        self.start_time = item['body']['start_time']

        self.currency_id = item['body']['currency_id']
        self.category_id = item['body']['category_id']
        self.user_id = item['body']['seller_id']

        currency_async = ml_api.currencies.get(item_id=item['body']['currency_id'])
        category_async = ml_api.categories.get(item_id=item['body']['category_id'])
        user_async = ml_api.users.get(item_id=item['body']['seller_id'])

        return True, [currency_async, category_async, user_async]

    def end_pipeline(self, ml_api):
        self.description = ml_api.currencies.get_from_cache(item_id=self.currency_id)['description']
        self.name = ml_api.categories.get_from_cache(item_id=self.category_id)['name']
        self.nickname = ml_api.users.get_from_cache(item_id=self.user_id)['nickname']

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

    def load_stages(self):
        self.tasks_pipeline = self.retrieve_item, self.retrieve_all_details

    def save(self, ml_api=None):
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
