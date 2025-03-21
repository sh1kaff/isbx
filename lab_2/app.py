from flask import Flask, jsonify, render_template, request

from src.utils import get_bits
from src.tests.tests import route_test


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index_handler():
    """Index Page"""
    return render_template("index.html")


@app.route("/gen/<lang>", methods=["GET"])
def gen_handler(lang):
    """Handler for generate bits string"""
    try:
        bits = get_bits(lang)
    except Exception as e:
        return jsonify({"error": str(e)})

    return jsonify({"lang": lang, "bits": bits})


@app.route("/test", methods=["POST"])
def test_handler():
    """Handler for test bits string with NIST"""
    try:
        data = request.get_json()

        test = data.get("test")
        bits = data.get("bits")
        result = route_test(test, bits)
    except Exception as e:
        return jsonify({"error": str(e)})

    return jsonify({"test": test, "result": result})


if __name__ == "__main__":
    app.run(debug=True)
