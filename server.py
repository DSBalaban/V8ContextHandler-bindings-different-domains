import tornado.ioloop
import tornado.web
import json
import os

def make_app():
    apps_folder = os.path.join(os.getcwd(), 'apps')
    return tornado.web.Application([
        (r"/(.*)", tornado.web.StaticFileHandler, { 'path': os.path.join(apps_folder) })
    ])

if __name__ == '__main__':
    app1 = make_app()
    app1.listen(8080)

    app2 = make_app()
    app2.listen(8081)

    tornado.ioloop.IOLoop.current().start()
