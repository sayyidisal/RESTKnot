from flask import Flask, session, request
from flask_socketio import Namespace, emit, disconnect
from command import read_rest
from app.middlewares.auth import login_required

class CommandNamespace(Namespace):
    def on_command(self, data):
        exec_com = read_rest(data)
        response={
            'data' : exec_com,
            "code": 200
        }
        emit('response', response)
        # disconnect()

    def on_get_person(self, message):
        emit('client',message, broadcast=True)


    def on_receive_person(self, data):
        # process your data on read rest or parsing
        # After Processing Data Send Response To Client
        response = {
            "code": 200,
            "messsages": "client-sync",
            "status": True
        }
        emit('client', response)

    def on_disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('client',
             {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()

    # def on_ping(self):
    #     emit('pong', 'pong')

    def on_connect(self):
        emit('client', {'data': 'Connected', 'client': request.sid})

    def on_disconnect(self):
        print('Client disconnected', request.sid)