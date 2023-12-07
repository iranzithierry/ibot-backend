import os
import json
from datetime import datetime

import Levenshtein

instagram_data_dir = "messages/inbox/"

ALL_MESSAGES = []

SENSITIVE_DATA = [
    "sent an attachment",
    "shared a story",
    "changed the theme",
    "can now message and call",
    "missed a",
    "wasn't notified about this message",
    "Liked a message",
    "You are now connected on Messenger",
    "missed your call",
    "You started a video chat",
    "Video chat ended",
    "You set the quick reaction to"
]


def calculate_similarity(one, two):
    ratio = Levenshtein.ratio(str(one).lower(), str(two).lower())
    return ratio


def encode_bytes_to_string(text_bytes: str):
    decodedString = text_bytes.encode("utf-8")
    realString = str(decodedString).split("'")[1].split("\\")
    normalStrings = ""
    for stringText in realString:
        if stringText.startswith("x"):
            if len(stringText[3:]) > 1:
                normalStrings = normalStrings + " " + stringText[3:]
        elif len(stringText) > 1:
            normalStrings = normalStrings + " " + stringText
    return normalStrings.strip()


def extract_data_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        participants = [participant["name"] for participant in data["participants"]]

        sender_receiver_messages = []
        current_message = None

        for message in data["messages"]:
            if len(participants) > 1:
                sender = message.get("sender_name", "Unknown")
                receiver = (
                    participants[0] if sender == participants[1] else participants[1]
                )
                content = (
                    message.get("content", "None") if "content" in message else "None"
                )
                timestamp_ms = message.get("timestamp_ms", 0)
                timestamp_ms = datetime.fromtimestamp(timestamp_ms / 1000.0).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                if current_message and current_message["sender"] == sender:
                    current_message[
                        "message"
                    ] = f"{content}, {current_message['message']}"
                else:
                    current_message = {
                        "sender": "Unknown"
                        if sender == ""
                        else sender.replace("Thierry Bronx", "Me").replace(
                            "T.Roy", "Me"
                        ),
                        "receiver": "Unknown"
                        if receiver == ""
                        else receiver.replace("Thierry Bronx", "Me").replace(
                            "T.Roy", "Me"
                        ),
                        "message": content,
                        "timestamp_ms": timestamp_ms,
                    }
                    sender_receiver_messages.append(current_message)

        sorted_messages = sorted(
            sender_receiver_messages, key=lambda x: x["timestamp_ms"], reverse=False
        )
        for message in sorted_messages:
            for category in ["receiver", "sender", "message"]:
                string = encode_bytes_to_string(message[category])
                if len(string) == 0:
                    message.pop(category, "")
            for sens_messages in SENSITIVE_DATA:
                similarity = calculate_similarity(message["message"], sens_messages)
                if similarity < 6:
                    message.pop("timestamp_ms", None)
                    ALL_MESSAGES.append(message)
        return ALL_MESSAGES


for folder_name in os.listdir(instagram_data_dir):
    folder_path = os.path.join(instagram_data_dir, folder_name)
    json_file_path = os.path.join(folder_path, "message_1.json")
    if os.path.exists(json_file_path):
        data = extract_data_from_json(json_file_path)
    else:
        data = {"data": "None"}

with open("data.json", "w") as outfile:
    json.dump(data, outfile, indent=4)

print(f"Structured  messages saved to '{outfile.name}'")
