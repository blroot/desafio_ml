from record.Record import Record
from fileupload.models import db, SiteIdPriceStartTimeNameDescriptionNickname
from HTTPApi.MLApi import MLApi
from typing import Iterable, Tuple, List


class SiteIdPriceStartTimeNameDescriptionNicknameRecord(Record):
    def __init__(self, values: List):
        self.site = values[0]
        self.id = values[1]
        self.price = ""
        self.start_time = ""
        self.name = ""
        self.description = ""
        self.nickname = ""
        self.currency_id = ""
        self.category_id = ""
        self.user_id = ""
        self.item_id = ""
        super(SiteIdPriceStartTimeNameDescriptionNicknameRecord, self).__init__(values)

    def retrieve_item(self, ml_api: MLApi) -> Iterable[Tuple] or None:
        if not self._id_valid() or not self._site_valid():
            self.cancel_pipeline()
            return

        item_async = ml_api.items.get(item_id=self._item_id(),
                                      extra_args='attributes=price,start_time,currency_id,category_id,seller_id')
        return [item_async]

    def retrieve_all_details(self, ml_api: MLApi) -> Iterable or None:
        item = ml_api.items.get_from_cache(item_id=self._item_id())
        if item['code'] != 200:
            self.cancel_pipeline()
            return

        if 'price' not in item['body'].keys():
            self.cancel_pipeline()
            return

        self.price = float(item['body']['price'])
        self.start_time = item['body']['start_time']

        self.currency_id = item['body']['currency_id']
        self.category_id = item['body']['category_id']
        self.user_id = item['body']['seller_id']

        currency_async = ml_api.currencies.get(item_id=item['body']['currency_id'], extra_args='attributes=description')
        category_async = ml_api.categories.get(item_id=item['body']['category_id'], extra_args='attributes=name')
        user_async = ml_api.users.get(item_id=item['body']['seller_id'], extra_args='attributes=nickname')

        return [currency_async, category_async, user_async]

    def end_pipeline(self, ml_api: MLApi):
        self.description = ml_api.currencies.get_from_cache(item_id=self.currency_id)['description']
        self.name = ml_api.categories.get_from_cache(item_id=self.category_id)['name']
        self.nickname = ml_api.users.get_from_cache(item_id=self.user_id)['nickname']

    def _site_valid(self) -> bool:
        return self.site in ['MLB', 'MLA']

    def _id_valid(self) -> bool:
        try:
            self.id = int(self.id)
        except ValueError:
            return False
        return True and self.id != ''

    def _item_id(self) -> str:
        return self.site + str(self.id)

    def load_stages(self) -> None:
        self.tasks_pipeline = self.retrieve_item, self.retrieve_all_details

    def save(self) -> None:
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
