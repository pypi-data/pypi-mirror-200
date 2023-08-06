import os
import requests
from threading import Thread
from queue import Queue
import crawles

q = Queue()


def image_get(url, data):
    html = requests.get(url, headers=head_data, params=data)
    for i in html.json()['data']['object_list']:
        print(i)




if __name__ == '__main__':
    for page_index in range(0, 121, 24):
        url = 'https://www.duitang.com/napi/blog/list/by_search/'
        # https://www.duitang.com/napi/blog/list/by_search/
        head_data = {
            # 字典，需要有一个键值对
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

        data = f'''
        kw: 美女
        after_id: {page_index}
        type: feed
        include_fields: like_count,sender,album,msg,reply_count,top_comments
        '''
        data = crawles.head_format(data)
        print(data)
        image_get(url, data)
        # Thread(target=image_get, args=(url, data)).start()

