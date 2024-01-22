import eventlet
import socketio
from datetime import datetime

class MyCustomNamespace(socketio.Namespace): # 名前空間を設定するクラス

    def on_connect(self, sid, environ):
        print('[{}] connet sid : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , sid))
        print('[{}] connet env : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , environ))
            
    def on_sid_message(self, sid, msg): # 送信してきたクライアントだけにメッセージを送る関数
        self.emit('response', msg, room=sid)
        print('[{}] emit sid : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , msg))

    def on_skip_sid_message(self, sid, msg):# 送信してきたクライアントを除く全ての接続しているクライアントにメッセージを送信する関数
        self.emit('response', msg, skip_sid=sid) 
        print('[{}] emit skip sid : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , msg))

    def on_broadcast_message(self, sid, msg):# 接続しているすべてのクライアントにメッセージを送る関数
        self.emit('response', msg)
        print('[{}] emit all : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , msg))
    
    def on_disconnect(self, sid):
        print('[{}] disconnect'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    
if __name__ == '__main__':
    
    sio = socketio.Server(cors_allowed_origins='*') # CORSのエラーを無視する設定
    sio.register_namespace(MyCustomNamespace('/test')) # 名前空間を設定
    app = socketio.WSGIApp(sio) # wsgiサーバーミドルウェア生成
    eventlet.wsgi.server(eventlet.listen(('',3000)), app) # wsgiサーバー起動
    