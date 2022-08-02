from flask import Flask,  request

from lib.path import PathManager
from lib.configparse import ConfigParse

import lib.database


config_parse = ConfigParse('config.ini')
db_detail = config_parse.read_database()
common = config_parse.read_common()


def create_app():
    db_object = lib.database.get_database(db_detail)
    path_manager = PathManager(db_object)
    app = Flask(__name__)

    @app.route('/')
    def home():
        index_page = open(
                        'static/index.html',
                        'r',
                        encoding='utf-8')
        return index_page.read(), 200

    @app.route('/<string:path>')
    def path_en(path):
        rdirect = path_manager.fetch(path)
        return rdirect

    @app.route('/new/', methods=['POST'])
    def new_link():
        link = request.form['url']
        return path_manager.path_add(link)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=common['serverHost'])
