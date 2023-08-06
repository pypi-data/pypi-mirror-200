import pymongo


class Mongo:
    def __init__(self):
        self.col = None
        self.cli = None
        self.db = None

    def connect(self,
                host='localhost',  # 主机名 127.0.0.1
                port=27017,  # 端口
                database=None,  # 需要连接的数据库名字
                table=None):

        if database is None or table is None:
            raise Exception('连接参数填写不完整!')

        self.cli = pymongo.MongoClient(host, port)
        self.db = self.cli[database]
        self.col = self.db[table]
        return self

    def insert_one(self, dict_mongo: dict):  # :dict 注解 提示作用
        """保存一条数据  {1:2}"""
        if not isinstance(dict_mongo, dict):
            raise Exception('数据不是字典类型')
        self.col.insert_one(dict_mongo)

    def insert_many(self, list_mongo: list):
        """保存多条数据 [{1:2},{2:3},{3:4}]"""
        if not isinstance(list_mongo, list):
            raise Exception('数据不是列表类型')

        for data in list_mongo:
            if not isinstance(data, dict):
                raise Exception('列表中的数据不是字典类型')

        self.col.insert_many(list_mongo)

    def close(self):
        self.cli.close()


mongo_save = Mongo()

if __name__ == '__main__':
    db = mongo_save.connect(host='localhost',  # 主机名 127.0.0.1
                            port=27017,  # 端口
                            database=None,  # 需要连接的数据库名字
                            table=None  # 连接表的名称
                            )

    dict_data = {'index': 1}
    db.insert_one(dict_data)  # 插入一条数据

    list_data = [{'index': 1}, {'index': 2}, {'index': 3}]
    db.insert_many(list_data)  # 插入多条数据

    db.close()  # 关闭数据库
