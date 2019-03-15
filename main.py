from flask import Flask, jsonify, request
from modules.wikipedia import Wikipedia
from raven.contrib.flask import Sentry

app = Flask(__name__)

sentry = Sentry(app)

wikipedia = Wikipedia()

"""
API version 1 routes
"""
# @app.route('/api/v1/search/<string:q>' , methods=['GET'])


@app.route('/api/v1/search')
def search():
    query = request.args.get('q')
    limit = request.args.get('limit')
    output = wikipedia.search(query, limit)
    return jsonify(output)


if __name__ == '__main__':
    app.run(port=5008)
