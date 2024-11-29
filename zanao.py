import json
import random
import os
import requests
from datetime import datetime
import pytz
import time

# 自行修改cookie与school_name
school_name = 'nepu'  # 学校英文缩写
cookies = {
    'user_token': 'XXXXX',
    'XXXXX',
    'XXXXX',
    'XXXXX',
}
headers = {
    'Host': 'c.zanao.com',
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Sc-Platform': 'android',
    'X-Sc-Alias': 'nepu',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090a13) XWEB/9129 Flue',
    'Referer': f'http://c.zanao.com/p/home?cid={school_name}',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
# 获取当前时间戳
timezone = pytz.timezone('Asia/Shanghai')
current_time = datetime.now(timezone)
timestamp_now = int(current_time.timestamp())

formatted_time = datetime.now().strftime("%Y%m%d%H%M")
file_path = f'/root/zanao/cron/files/{formatted_time}.txt'

# 检查文件是否存在，如果不存在则创建文件
if not os.path.isfile(file_path):
    with open(file_path, 'w', encoding='utf8') as fp:
        pass  # 可以添加一些初始内容，或者直接留空

# 获取时间戳对应的页面的所有tid
def get_tid(timestamp):
    tid_url = f'http://c.zanao.com/sc-api/thread/v2/list?from_time={timestamp}&hot=1&isIOS=false'
    response_tid = requests.get(
        url=tid_url,
        cookies=cookies,
        headers=headers
    )
    data = response_tid.json()

    tid_dict={i['thread_id']:{'title':i['title'],'time':i['p_time'],'nickname':i['nickname']} for i in  data['data']['list']}
    # print(tid_dict)
    return tid_dict
# 以json格式存储帖子tid与title在txt中
def save_txt(tid_dict):
    with open(file_path,'r+',encoding='utf8') as fp:
        old=fp.read()
        if len(old)!=0:
            old_json=json.loads(old)
            keys_set=set(list(old_json.keys())+list(tid_dict.keys()))
            new=old_json.copy()
            for key in tid_dict.keys():
                new[key]=tid_dict[key]
            diff={key:new[key] for key in set(new.keys())-set(old_json.keys())}
            print('diff',diff)
            fp.seek(0)
            fp.write(json.dumps(new))

        else:
            fp.write(json.dumps(tid_dict))

for num in range(49):
    tid_dict = get_tid(timestamp_now-num*1800)
    # 以json格式存储帖子tid与title在txt中
    save_txt(tid_dict)
    time.sleep(random.randrange(0,4))