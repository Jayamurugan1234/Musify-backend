# import json

# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):

#     async def connect(self):

#         # self.user = self.scope["user"]

#         # if self.user.is_anonymous:

#         #     await self.close()

#         # else:

#         #     self.group_name = f"user_{self.user.id}"

#         #     await self.channel_layer.group_add(
#         #         self.group_name,
#         #         self.channel_name
#         #     )

#         #     await self.accept()

#         await self.accept()

#         await self.send(
#             text_data=json.dumps({
#                 "message": "WebSocket Connected"
#             })
#         )

#     async def disconnect(self, close_code):

#         # await self.channel_layer.group_discard(
#         #     self.group_name,
#         #     self.channel_name
#         # )
#         pass

#     async def receive(self, text_data):

#         pass

#     async def send_notification(self, event):

#         await self.send(
#             text_data=json.dumps({
#                 "message": event["message"]
#             })
#         )





# import json

# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):

#     async def connect(self):

#         await self.accept()

#         await self.send(
#             text_data=json.dumps({
#                 "message": "WebSocket Connected"
#             })
#         )

#     async def disconnect(self, close_code):
#         pass




# import json

# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):

#     async def connect(self):

#         await self.accept()

#         await self.send(
#             text_data=json.dumps({
#                 "message": "WebSocket Connected"
#             })
#         )

#     async def disconnect(self, close_code):
#         pass




# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):

#     async def connect(self):

#         print("WEBSOCKET CONNECT ATTEMPT")

#         await self.accept()

#         await self.send(
#             text_data=json.dumps({
#                 "message": "WebSocket Connected"
#             })
#         )

#     async def disconnect(self, close_code):
#         print("WEBSOCKET DISCONNECTED")


# import json

# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):

#     async def connect(self):

#         print("WEBSOCKET CONNECT ATTEMPT")

#         await self.accept()

#         await self.send(
#             text_data=json.dumps({
#                 "message": "WebSocket Connected"
#             })
#         )

#     async def disconnect(self, close_code):

#         print("WEBSOCKET DISCONNECTED")


# import json

# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):

#     # async def connect(self):

#     #     user = self.scope["user"]

#     #     if user.is_anonymous:
#     #         await self.close()
#     #         return

#     #     self.group_name = f"user_{user.id}"

#     #     await self.channel_layer.group_add(
#     #         self.group_name,
#     #         self.channel_name
#     #     )

#     #     await self.accept()

#     #     await self.send(
#     #         text_data=json.dumps({
#     #             "message": "WebSocket Connected"
#     #         })
#     #     )


#     async def connect(self):

#         print("WEBSOCKET CONNECTED")

#         self.group_name = "user_1"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.accept()

#         await self.send(
#             text_data=json.dumps({
#                 "message": "WebSocket Connected"
#             })
#         )

#     async def disconnect(self, close_code):

#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     # async def send_notification(self, event):

#     #     await self.send(
#     #         text_data=json.dumps({
#     #             "message": event["message"]
#     #         })
#     #     )


#     async def send_notification(self, event):

#         print("NOTIFICATION RECEIVED:", event)

#         await self.send(
#             text_data=json.dumps({
#                 "message": event["message"]
#             })
#         )



# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):

#     # async def connect(self):

#     #     self.user = self.scope["user"]

#     #     # TEMP FIX (IMPORTANT FOR TESTING)
#     #     # bypass auth issues
#     #     self.user_id = 1

#     #     self.group_name = f"user_{self.user_id}"

#     #     await self.channel_layer.group_add(
#     #         self.group_name,
#     #         self.channel_name
#     #     )

#     #     await self.accept()

#     #     await self.send(text_data=json.dumps({
#     #         "message": "WebSocket Connected"
#     #     }))

#     #     print("CONNECTED + GROUP:", self.group_name)


#     async def connect(self):

#         self.user_id = 1   # FORCE TEST USER

#         self.group_name = f"user_{self.user_id}"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.accept()

#         await self.send(text_data=json.dumps({
#             "message": "WebSocket Connected"
#         }))

#         print("CONNECTED + GROUP:", self.group_name)

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def send_notification(self, event):

#         print("RECEIVED EVENT:", event)

#         await self.send(text_data=json.dumps({
#             "message": event["message"]
#         }))



# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         self.user_id = 1
#         self.group_name = "test_group"

#         await self.accept()

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         print("CONNECTED:", self.group_name)

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#         print("DISCONNECTED")

#     async def receive(self, text_data):
#         print("RECEIVED FROM CLIENT:", text_data)

#     async def send_notification(self, event):
#         print("🔥 EVENT RECEIVED:", event)

#         await self.send(text_data=json.dumps({
#             "message": event.get("message")
#         }))



# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         self.group_name = "test_group"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.accept()

#         print("CONNECTED TO:", self.group_name)

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def send_notification(self, event):
#         print("🔥 EVENT RECEIVED:", event)

#         await self.send(text_data=json.dumps({
#             "message": event["message"]
#         }))


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         print("CONNECT CALLED")

#         await self.accept()

#         print("ACCEPTED SUCCESSFULLY")

#     async def receive(self, text_data):
#         print("MESSAGE FROM BROWSER:", text_data)

#         await self.send(text_data=json.dumps({
#             "message": "HELLO FROM DJANGO WORKS 🎵"
#         }))

#     async def disconnect(self, close_code):
#         print("DISCONNECTED:", close_code)



# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         print("CONNECT HIT")
#         await self.accept()
#         print("ACCEPT DONE")

#     async def disconnect(self, close_code):
#         print("DISCONNECT:", close_code)


# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         print("CONNECT HIT")
#         await self.accept()
#         print("ACCEPT DONE")

#     async def disconnect(self, close_code):
#         print("DISCONNECTED:", close_code)



from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("CONNECT HIT")
        await self.accept()
        print("ACCEPT DONE")

        # send immediate message back (important test)
        await self.send(text_data="HELLO FROM DJANGO")

    async def disconnect(self, close_code):
        print("DISCONNECTED:", close_code)