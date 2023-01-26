from flask import request, session
from flask_socketio import Namespace, emit, join_room, leave_room

from . import db

class clientManager:
    def duplication():
        roomData = db.child('clientRooms').child(session['roomName']).get()
        if roomData.val() is not None:
            for value in roomData.each():
                if value.val()['clientName'] == session['playerName']:
                        db.child('clientRooms').child(session['roomName']).child(str(value.key())).update({'clientId': request.sid})
                        join_room(session['roomName'], sid=request.sid)
                        return True
                
            return False
    
    def client_leave():
        roomData = db.child('clientRooms').child(session['roomName']).get()
        if roomData.val() is not None:
            for value in roomData.each():
                if value.val()['clientName'] == session['playerName']:
                        db.child('clientRooms').child(session['roomName']).child(str(value.key())).remove()
                        leave_room(session['roomName'], sid=request.sid)
                        
                        return True


class RoomServices(Namespace):
    def on_connect(self):
        print('[CLIENT CONENCTED]:',request.sid)
        print('ACTIVE CLIENT',session)

    def on_disconnect(self):
        if clientManager.client_leave():
            session.clear()
            print('[CLIENT DISCONENCTED]:',request.sid)
            print('ACTIVE CLIENT',session)


    def on_room_request(self):
        if not clientManager.duplication():
            db.child('clientRooms').child(session['roomName']).push({'clientId':request.sid, 'clientName': session['playerName'], 'clientRoom': session['roomName']})
            join_room(session['roomName'], sid=request.sid)

        roomData = db.child('clientRooms').child(session['roomName']).get()
        emit('room_response', dict(roomData.val()), to=session['roomName'], broadcast=True)
    
    def on_set_items(self, data, roomName):
        emit('load_items', data, to=roomName, broadcast=True)


    def on_prepare_set(self,data,roomName):
        emit('pre_sets', {'id':request.sid, 'data':data}, to=roomName, broadcast=True) 
        emit('btn_activator', 'all', to=roomName, broadcast=True)

    def on_backup_loader(self, data, roomName):
        print(data)
        emit('backup', data, to=roomName, broadcast=True) 


