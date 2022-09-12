from flask import Flask,  request

from src.path import PathManager
from src.configparse import ConfigParse

import src.database


config_parse = ConfigParse('config.ini')
db_detail = config_parse.read_database()
common = config_parse.read_common()


def create_app():
    db_object = src.database.get_database(db_detail)
    path_manager = PathManager(db_object)
    flask_app = Flask(__name__)

    @flask_app.route('/')
    def home():
        index_page = open(
                        'static/index.html',
                        'r',
                        encoding='utf-8')
        return index_page.read(), 200

    @flask_app.route('/<string:path>')
    def path_en(path):
        rdirect = path_manager.fetch(path)
        return rdirect

    @flask_app.route('/new/', methods=['POST'])
    def new_link():
        link = request.form['url']
        return path_manager.path_add(link)

    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(host=common['serverHost'])
