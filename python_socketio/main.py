from webapplication import create_server 

app, sio = create_server()


@app.route('/test')
def index():
    return 'flask socketio runnning......'

if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', port=5000, debug=True)