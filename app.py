from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session, send_file
import musicController
from flask_sockets import Sockets
import datetime
import time
import main
app = Flask(__name__, static_url_path='/static')
sockets = Sockets(app)

songController = musicController.controller()

for val in musicController.EXAMPLE_SONGS:
	songInfo = musicController.parseURL(val)
	songController.add(vars(songInfo))

print songController.order
'''
for i, val in enumerate(songController.order):
	print("{} - {}".format(i, val['song']))

for i in range(5):
	song = songController.play_next()
	print("Playing: {} | Next Song: {}".format(song, songController.get_next()))

'''

@app.route("/postRequest", methods=["POST"])
def post_request():
	#print request.data
	#print request.get_json
	url = dict(request.form).keys()[0].partition("?")[0]
	returnedData = musicController.parseURL(url, download=True)
	x = vars(returnedData)
	main.addToDB(x)
	songController.add(x)
	return 'This works'

@app.route("/getSongOrder", methods=["GET"])
def get_song_order():
	b = ""

	a = ""
	for val in songController.order[1:]:
		a += '''
		<li href="#">
				<div class="song-detail">
				  <div class="row">
					<div class="col">
					  <h3>{}</h3>
					  <p>{} | {}</p>
					</div>
					<div class="col">
					  <div class="row mx-auto float-right float-right">
						<a onclick="document.getElementById('up1').src='/static/upactive.png'; document.getElementById('down1').src='down.png'"><img id="up1" src="/static/up.png" class="arrow"/></a>
						<a onclick="document.getElementById('up1').src='/static/up.png'; document.getElementById('down1').src='/static/downactive.png'"><img id="down1" src="/static/down.png" class="arrow "/></a>
					  </div>
					</div>
				  </div>
				</div>
			  </li>
		'''.format(val['song'], val['artist'], val['album'])
	return a

@sockets.route('/echo')
def echo_socket(ws):
	prevValue = None
	while True:
		# print songController.order
		if str(songController.order) != str(prevValue):
			ws.send(str(datetime.datetime.now()))
			prevValue = str(songController.order)
		time.sleep(.1)
		


@app.route("/getCurrent", methods=["GET"])
def get_current_info():
	if len(songController.order) == 0:
		return ""
	currentSong = songController.order[0]
	a = """<div class="row">
			  <h1>{}</h2>
			</div>
			<div class="row">
			  <h3>{} | {}</h3>
			</div>
			""".format(currentSong['song'], currentSong['artist'], currentSong['album'])
	return a

@app.route("/getCurrentAlbumArtwork", methods=["GET"])
def get_current_album_artwork():
	if len(songController.order) == 0:
		return ""
	return songController.order[0]['album_art']

@app.route('/addSong', methods=["POST"])
def index():
	data = request.get_json()
	url = data['url']
	returnedData = musicController.parseURL(url, download=True)
	# raw_input(vars(returnedData))
	#returnedData = parseURL(url, download=True)
	x = vars(returnedData)
	main.addToDB(x)
	songController.add(x)
	return 'This works'

@app.route('/playCurrent', methods=["GET"])
def play_current_song():
	return send_file("songs/{}.mp3".format(songController.play_current()))
	
@app.route('/playNext', methods=["GET"])
def play_next_song():
	songController.play_next()
	return "playing next song"
	return send_file("songs/{}.mp3".format(songController.play_current()))
	


@app.route('/test', methods=['GET'])
def testPage():
	return render_template("index1.html")

@app.route('/player', methods=['GET'])
def getPlayer():
	if len(songController.order) == 0:
		nowPlaying = None
	else:
		nowPlaying = songController.order[0]
	return render_template("player.html", nowPlaying=nowPlaying, songList=songController.order[1:])

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000)
