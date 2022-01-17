from distutils.core import setup
from logging import debug
from flask import Flask, json, request, jsonify, abort

from models import setup_db, Greeting
from flask_cors import CORS

app = Flask(__name__)
setup_db(app)

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
cors = CORS(app, resources={"*": {"origins": "*"}})

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
    # TODO implement pagination
    greetings = Greeting.query.all()
    greetings = [greeting.format() for greeting in greetings]
    return jsonify({'greetings': greetings})


@app.route('/greetings/<lang>', methods=['GET'])
def greeting_one(lang):
    greeting = Greeting.query.filter_by(lang == lang)
    print(lang)
    # if(lang not in greetings):
    if(not greeting):
        return jsonify({'error': "no greeting in this language"})
    return jsonify({'greeting': greeting})


@app.route('/greetings', methods=['POST'])
def greeting_add():
    info = request.get_json()
    if('lang' not in info or 'greeting' not in info):
        abort(422)
    # greetings[info['lang']] = info['greeting']
    greeting = Greeting(info['lang'], info['greeting'])
    greeting.insert()
    return jsonify({'greeting': greeting.format()})

if __name__ == "__main__":
    app.run(debug=True)
