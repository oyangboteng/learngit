from tornado import web, ioloop, httpserver
import json
import numpy as np
import cv2


# tornado 是顺序调用的，当其中一个handler(比如post)正在运行还没返回结果的时候。调用其它handler是没有反应的，如果需要就得用携程编程

# 按 json 格式传递数据
class Request_Json_Handler(web.RequestHandler):

    #post json格式数据，会产生跨域问题，会先进行options请求，加options处理（将所有options请求放行）
    def options(self):
        self.set_header("Access-Control-Allow-Origin", '*')
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE")
        self.set_header("Access-Control-Allow-Headers", "content-type,x-requested-with,Authorization, x-ui-request,lang")
        #返回方法1
        self.set_status(200)
        self.finish()
        #返回方法2
        # print(self.request)
        # print(self.request.headers)
        # print(self.request.body)
        # self.write('{"errorCode":"00","errorMessage","success"}')

    def post(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):#需要先判断请求体的数据是否为 application/json 格式：
            app = self.application
            state = app._state
            state = 1
            # info_dic = json.loads(self.request.body.encode('utf-8'))
            # 这是因为，python3中，编码的时候区分了字符串和二进制
            # encode 改为 decode 就可以了 参数默认utf-8
            info_dic = json.loads(self.request.body.decode('utf-8'))
            print(type(info_dic))
            print(info_dic)

            respond_dic = {"code": 1,  "state": state, "msg": "recive json success ..."}

            self.finish(respond_dic)
        else:
            print('request not json')


# 按 formdata 格式传递数据
class Request_formdata_Handler(web.RequestHandler):

    def post(self):

        app = self.application
        state = app._state
        state = 2

        # sid = self.request.arguments["session_id"][0].encode('utf-8')
        sid = self.request.arguments["session_id"][0].decode('utf-8')
        print(sid)

        file_metas = self.request.files["pic"]
        for meta in file_metas:
            file_content = meta["body"]
            img = np.frombuffer(file_content, dtype=np.uint8)
            img = cv2.imdecode(img, 1)
            print(img)

        respond_dic = {"code": 1, "state": state, "msg": "recive formdata success ..."}

        self.finish(respond_dic)


# 带参数请求
class Get_State_Handler(web.RequestHandler):

    def get(self, sid):

        print(sid)

        app = self.application
        state = app._state
        state = 3

        respond_dic = {"code": 1, "state": state, "msg": "recive body success ..."}

        self.finish(respond_dic)


class Application(web.Application):

    def __init__(self):

        handler = [

            (r'/process/request_json', Request_Json_Handler),
            (r'/process/request_formdata', Request_formdata_Handler),
            (r'/process/get_state/?(?P<sid>.+)?', Get_State_Handler)
        ]

        web.Application.__init__(self, handlers=handler)

        # 全局变量
        # 只有写在这里才可以所有handler公用，写在外面不管用
        self._state = 0


def make_app():

    ioloop_t = ioloop.IOLoop()

    httpserver_t = httpserver.HTTPServer(Application())

    httpserver_t.listen(8889)

    ioloop_t.start()


if __name__ == "__main__":

    make_app()

