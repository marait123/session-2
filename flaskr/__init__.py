from logging import debug
from flask import Flask, json, request, jsonify, abort


app = Flask(__name__)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    greetings = {
        'en': 'hello',
        'es': 'Hola',
        'ar': 'مرحبا',
        'ru': 'Привет',
        'fi': 'Hei',
        'he': 'שלום',
        'ja': 'こんにちは'
    }

    @app.route('/', methods=['GET'])
    def index():
        return "<h1>hello friends</h1>"

    @app.route('/greeting', methods=['GET'])
    def greeting_all():
        # TODO implement pagination
        return jsonify({'greetings': greetings})

    @app.route('/greeting/<lang>', methods=['GET'])
    def greeting_one(lang):
        print(lang)
        if(lang not in greetings):
            abort(404)
        return jsonify({'greeting': greetings[lang]})

    @app.route('/greeting', methods=['POST'])
    def greeting_add():
        info = request.get_json()
        if('lang' not in info or 'greeting' not in info):
            abort(422)
        greetings[info['lang']] = info['greeting']
        return jsonify({'greetings': greetings})
    return app
