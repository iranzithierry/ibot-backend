import os
import json
from datetime import datetime

instagram_data_dir = 'messages/inbox/'

all_messages = []


def extract_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        participants = [participant["name"] for participant in data["participants"]]

        sender_receiver_messages = []
        current_message = None

        for message in data['messages']:
            if len(participants) > 1:
                sender = message.get("sender_name", "Unknown")
                receiver = participants[0] if sender == participants[1] else participants[1]
                content = message.get("content", "None") if "content" in message else "None"
                timestamp_ms = message.get("timestamp_ms", 0)
                timestamp_ms = datetime.fromtimestamp(timestamp_ms / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
    
                if current_message and current_message['sender'] == sender:
                    current_message['message'] = f"{content}, {current_message['message']}"  # Reverse the order
                else:
                    current_message = {
                        'sender': "Unknown" if sender == '' else sender.replace("Thierry Bronx","Me").replace("T.Roy","Me"),
                        'receiver': "Unknown" if receiver == '' else receiver.replace("Thierry Bronx","Me").replace("T.Roy","Me"),
                        'message': content,
                        'timestamp_ms': timestamp_ms
                    }
                    sender_receiver_messages.append(current_message)


        sorted_messages = sorted(sender_receiver_messages, key=lambda x: x['timestamp_ms'], reverse=False)
        for message in sorted_messages:
            if "sent an attachment" not in message['message'] and "shared a story" not in message['message']:
                if "changed the theme" not in message['message'] and "missed a" not in message['message']:
                    if "can now message and call" not in message['message'] and "missed a" not in message['message']:
                        if "wasn't notified about this message" not in message['message'] and "Liked a message" not in message[
                            'message']:
                            message.pop("timestamp_ms", None)
                            all_messages.append(message)
        return all_messages


for folder_name in os.listdir(instagram_data_dir):
    folder_path = os.path.join(instagram_data_dir, folder_name)
    json_file_path = os.path.join(folder_path, 'message_1.json')
    if os.path.exists(json_file_path):
        data = extract_data_from_json(json_file_path)
    else:
        data = {"data": "None"}

with open('data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

print(f"Structured  messages saved to '{outfile.name}'")
