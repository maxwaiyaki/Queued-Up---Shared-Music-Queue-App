from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
from spotify import parseURL

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET', "POST"])
def index():
	data = request.get_json()
	url = data['url']
	returnedData = parseURL(url)
	return jsonify(returnedData.return_values())
	print request.get_json()
	return jsonify(data)

@app.route('/test', methods=['GET'])
def testPage():
	return render_template("index1.html")

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000)