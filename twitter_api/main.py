import json
from flask import jsonify, Flask, request
from model.twit import Twit

twits = []
app = Flask(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Twit):
            return {"body": obj.body, "author": obj.author}
        else:
            return super().default(obj)

app.json_encoder = CustomJSONEncoder

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"response": "pong"})


@app.route("/twit", methods=["POST"])
def create_twit():
    twit_json = request.get_json()
    if 'body' in twit_json and 'author' in twit_json:
        twit = Twit(twit_json["body"], twit_json["author"])
        twits.append(twit)
        return jsonify({"response": "success"})
    else:
        return jsonify({"error": "Нет enough data to create a new tweet."}), 400


@app.route("/twit", methods=["PATCH"])
def change_twit():
    twits.pop()
    twit_json = request.get_json()
    if 'body' in twit_json and 'author' in twit_json:
        twit = Twit(twit_json["body"], twit_json["author"])
        twits.append(twit)
        return jsonify({"response": "success"})
    else:
        return jsonify({"error": "Нет enough data to create a new tweet."}), 400


@app.route("/twit", methods=["DELETE"])
def pop_twit():
    twits.pop()
    return jsonify({"response": "success"})


@app.route("/twit", methods=["GET"])
def read_twit():
    return jsonify([tweet.to_dict() for tweet in twits])

if __name__ == "__main__":
    app.run(debug=True)

# class Twit:
#     def __init__(self, body, author):
#         self.body = body
#         self.author = author
#
#     def to_dict(self):
#         return {"body": self.body, "author": self.author}
