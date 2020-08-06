import requests
import time

# url = 'http://127.0.0.1:8899/search_user'
# name = 'aaa'
# password = '123456'
# dara_farm = {
#         'username':name,
#         'token':password
# }
#
# tag = requests.post(url, data= dara_farm)
# # tag.encoding('utf-8')
# tag = tag.text
# print(tag)

import requests
import json


json_url = 'http://127.0.0.1:8889/process/request_json'
formdata_url = 'http://127.0.0.1:8889/process/request_formdata'
get_url = 'http://127.0.0.1:8889/process/get_state'
test_url = 'http://127.0.0.1:8832/post'



def request_json():

    info_dic = {"session_id": 1, "motion":"高兴"}

    respon = requests.post(json_url, data = json.dumps(info_dic))

    # ???? encode 好像对字典不起作用
    # r_dic = json.loads(respon.content.encode('utf-8'))
    r_dic = json.loads(respon.content.decode('utf-8'))
    # r_dic = respon.text

    print(r_dic)


def request_formdata():

    session_id = 2

    pic_path = "D:/shujubao/001.jpg"

    # formdata = {
    #     'pic': ('/home/gunn/csdn/1.png', open('/home/gunn/csdn/1.png', 'rb')),
    #     'session_id': (None, str(session_id)),
    # }
    formdata = {
        'pic': (pic_path, open(pic_path, 'rb')),
        'session_id': (None, str(session_id)),
    }
    respons = requests.post(formdata_url, files=formdata)

    # ???
    # r_dic = json.loads(respons.content.encode('utf-8'))
    r_dic = json.loads(respons.content.decode('utf-8'))

    print(r_dic)


def get_state():

    session_id = '33'

    url = get_url + '/' + session_id

    respons = requests.get(url)

    r_dic = json.loads(respons.content.decode("utf-8"))

    print(r_dic)

def api_test_url():
    info_dic = {"a": 1, "b":2}
    params = {
        'a': '1',
        'b': '2'
    }
    headers = {
        "Content-Type":"application/json; charset=utf-8"
    }
    params = json.dumps(params,ensure_ascii=False)
    respon = requests.post(test_url, data = params, headers = headers)

    # ???? encode 好像对字典不起作用
    # r_dic = json.loads(respon.content.encode('utf-8'))
    r_dic = json.loads(respon.content.decode('utf-8'))
    # r_dic = respon.text

    print(r_dic)

if __name__ == "__main__":

    # request_json()

    # request_formdata()
    #
    # get_state()
    api_test_url()
