from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# def send_realtime_notification(user_id, message):

#     print("Sending notification to:", user_id)

#     channel_layer = get_channel_layer()

#     async_to_sync(channel_layer.group_send)(
#         f"user_{user_id}",
#         {
#             "type": "send_notification",
#             "message": message
#         }
#     )


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_realtime_notification(group_name, message):

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "message": message
        }
    )