import json
import time
from scan import crawl
from hashlib import md5
from scan.common import logger


class Monitor:
    def __init__(self):
        self.__logs = {}

    def _need_send(self, send_data):
        data_md5 = md5(json.dumps(send_data).encode()).hexdigest()
        now = int(time.time())
        for k, v in self.__logs.items():
            if v + 60 * 30 < now:
                self.__logs.pop(k)
        if self.__logs.get(data_md5):
            return False
        else:
            self.__logs.update({data_md5: int(time.time())})
            return True

    async def send_warn_fs(self, web_hook_url, product_name, message, at='', uid=''):
        post_data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "爬虫项目异常推送",
                        "content": [
                            [{"tag": "text", "text": f"项目:【{product_name}】"}],
                            [{"tag": "text", "text": f"描述: {message}"}],
                            [{"tag": "text", "text": f"项目负责人:@{at}"}]
                        ]
                    }
                }
            }
        }
        if not self._need_send(post_data):
            return
        try:
            resp = await crawl.fetch(web_hook_url, json=post_data)
            data = resp.json()
            logger.info(f'告警返回:{data}')
        except Exception as e:
            logger.error(f'发送告警数据异常:{e}')

    async def async_check_mysql_update_time(self, conn, db, table):
        pass

    def check_mysql_update_time(self, conn, db, table):
        pass


monitor = Monitor()
__all__ = monitor
