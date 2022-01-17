from distutils.core import setup
from logging import debug
from flask import Flask, json, request, jsonify, abort

from models import setup_db, Greeting
from flask_cors import CORS
Page_count=2
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    cors = CORS(app, resources={"*": {"origins": "*"}})

    # example greetings
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


    @app.route('/greetings', methods=['GET'])
    def greeting_all():
        page = request.args.get('page',1, type=int)
        pagination = Greeting.query.paginate(page, per_page=Page_count,error_out=False)
        greetings = pagination.items
        # TODO implement pagination
        # greetings = Greeting.query.all()
        greetings = [greeting.format() for greeting in greetings]
        return jsonify({'greetings': greetings, 'count':pagination.total})



    @app.route('/greetings/<lang>', methods=['GET'])
    def greeting_one(lang):
        greeting = Greeting.query.filter_by(lang = lang).first()
        print(lang)
        # if(lang not in greetings):
        if(not greeting):
            return jsonify({'error': "no greeting in this language"})
        return jsonify({'greeting': greeting.format()})


    @app.route('/greetings', methods=['POST'])
    def greeting_add():
        info = request.get_json()
        if('lang' not in info or 'greeting' not in info):
            abort(422)
        # greetings[info['lang']] = info['greeting']
        greeting = Greeting(info['lang'], info['greeting'])
        greeting.insert()
        return jsonify({'greeting': greeting.format()})
    return app
    # if __name__ == "__main__":
    #     app.run(debug=True)
