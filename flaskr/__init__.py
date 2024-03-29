from distutils.core import setup
from logging import debug
from flask import Flask, json, request, jsonify, abort

from models import setup_db, Greeting
from flask_cors import CORS
from flask_migrate import Migrate

Page_count = 2


def create_app(test_config=None):
    app = Flask(__name__)
    db = setup_db(app)
    migrate = Migrate(app, db) # this line
    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    cors = CORS(app,   resources={"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS'
        )
        return response
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
        page = request.args.get('page', 1, type=int)
        pagination = Greeting.query.paginate(
            page, per_page=Page_count, error_out=False)
        greetings = pagination.items
        # TODO implement pagination
        # greetings = Greeting.query.all()
        greetings = [greeting.format() for greeting in greetings]
        return jsonify({'greetings': greetings, 'count': pagination.total})

    @app.route('/greetings/<lang>', methods=['GET'])
    def greeting_one(lang):
        greeting = Greeting.query.filter_by(lang=lang).first()
        print(lang)
        # if(lang not in greetings):
        if(not greeting):
            abort(404)
        return jsonify({'greeting': greeting.format()})

    @app.route('/greetings', methods=['POST'])
    def greeting_add():
        info = request.get_json()
        if('lang' not in info or 'greeting' not in info):
            abort(422)
        # greetings[info['lang']] = info['greeting']
        greeting = Greeting(info['lang'], info['greeting'])
        greeting.insert()
        return jsonify({'greeting': greeting.format()}), 201

    # TODO: implement beautifull greeting
    @app.route('/greetings/<lang>/beautiful', methods=['POST'])
    def beautiful_greeting(lang):
        greeting = "namastai"
        return jsonify({'greeting': f'greeting in language {lang} is {greeting}'})

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
        }), 422

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "message": "resource not found",
            "success": False,
            "error": 404,
        }), 404
    return app
    # if __name__ == "__main__":
    #     app.run(debug=True)
