from typing import Text, Optional
from typing import Union, Iterable

from .CsvSave import CsvSave
from .Mongo import Mongo
from .MySQL import SqlSave


class DataSave:
    def image_save(image_url: Text,
                   image_path: Union[Text, bytes],
                   astrict: Optional = 100,
                   **kwargs):
        pass

    def images_save(image_iteration: Iterable[Iterable[Text, Text]],
                    astrict: Optional = 100,
                    **kwargs): pass

    mongo_save = Mongo()
    sql_save = SqlSave()

    def csv_save(self, filename, mode='r+',
                 encoding='gbk',
                 newline='',
                 **kwargs) -> CsvSave: pass


data_save = DataSave
