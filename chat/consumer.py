import json

from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    # 새 연결이 수신되었을때 호출
    def connect(self):
        # 모든 연결 수락
        self.accept()
    
    # 소켓이 닫힐 때 호출
    def disconnect(self, close_code):
        pass

    # receive()는 데이터를 수신할 때마다 호출
    # WebSocket에서 메시지 수신
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # 메시지를 WebSocket으로 전송
        self.send(text_data=json.dumps({'message':message}))