from flask import Blueprint, render_template, request, redirect, url_for, session
from . import TEMPLATE_PATH
from . import firebase_init

views = Blueprint('views', __name__)
# clientRoom = firebase_init()

@views.route('/')
def landing():
	return render_template('AL_index.html')

@views.route('/lobby')
def lobby():
	return render_template('ALchoose.html')

@views.route('/host', methods=['GET', 'POST'])
def host():
	if request.method == 'POST':
		session['playerName'] = request.form.get('player-name')+" (host)"
		session['roomName'] = request.form.get('room-name').lower()

		if session['playerName'] and session['roomName']:
			return redirect(url_for('.room'))
		else:
			return redirect(url_for('.host'))
	else:    
		return render_template('ALnew.html')

@views.route('join', methods=['GET', 'POST'])
def join():
	if request.method == 'POST':
		session['playerName'] = request.form.get('player-name')
		session['roomName'] = request.form.get('room-name').lower()

		if session['playerName'] and session['roomName']:
			return redirect(url_for('.room'))
		else:
			return redirect(url_for('.join'))
	else:    
		return render_template('ALjoin.html')


@views.route('/room')
def room(): 
	return render_template('room.html', hostRoom=session['roomName'], hostPlayer=session['playerName'])