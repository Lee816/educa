import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    # 새 연결이 수신되었을때 호출
    def connect(self):
        # scope에서 course_id 매개변수를 검색하여 채팅방이 연결된 강의를 알아낸다.
        self.id = self.scope['url_route']['kwargs']['course_id']
        # 각 강의 채팅방에 대해 채널 그룹을 생성
        self.room_group_name = f'chat_{self.id}'
        # 현재 채널에 그룹을 추가하고 그룹에 참여
        async_to_sync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)
        # 모든 연결 수락
        self.accept()
    
    # 소켓이 닫힐 때 호출
    def disconnect(self, close_code):
        # 그룹에서 나가기
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    # receive()는 데이터를 수신할 때마다 호출
    # WebSocket에서 메시지 수신
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # 메시지를 WebSocket으로 전송
        #self.send(text_data=json.dumps({'message':message}))
        # 그룹에 메시지 보내기
        async_to_sync(self.channel_layer.group_send)(self.room_group_name,{
            'type' : 'chat_message', # type : 이벤트 타입, 특별한 키로 해당하는 이벤트를 받는 컨슈머에서 실행되어야 할 메서드의 이름과 일치해야한다.
            'message' : message,
        })
        
    # 그룹에서 메시지 받기
    def chat_message(self, event):
        # WebSocket으로 메시지 보내기
        self.send(text_data=json.dumps(event))