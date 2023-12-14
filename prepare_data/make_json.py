import os
import json
from datetime import datetime
from pathlib import Path
import re
import Levenshtein
import asyncio

INBOX_DIR = Path("../data_classified/inbox/")

ALL_MESSAGES = []
NEW_MESSAGES = []
SENSITIVE_DATA = [
    "Liked a message",
    "sent an attachment",
    "You sent an attachment.",
    "liked a message" "shared a story",
    "changed the theme",
    "can now message and call",
    "missed a",
    "wasn't notified about this message",
    "You are now connected on Messenger",
    "missed your call",
    "You started a video chat",
    "Video chat ended",
    "You set the quick reaction to",
]


class MakeJson:
    def __init__(self, inbox_dir: Path):
        """
        Initializes the FileManager with the specified directories and paths.
        """
        self.inbox_dir = inbox_dir
        self.inboxes_dir = os.listdir(inbox_dir)

    def encode_bytes_to_string(self, text_bytes: str):
        decodedString = text_bytes.encode("utf-8")
        realString = str(decodedString).split("'")[1].split("\\")
        normalStrings = ""
        for stringText in realString:
            if stringText.startswith("x"):
                if len(stringText[3:]) > 1:
                    normalStrings = normalStrings + " " + stringText[3:]
            elif len(stringText) > 1:
                normalStrings = normalStrings + " " + stringText
        lastString = normalStrings.strip()
        if len(lastString) == 0:
            lastString = ""
        return lastString

    def get_sender(self, message):
        sender = message.get("sender_name", "Unknown")
        sender = self.encode_bytes_to_string(sender)
        names = ["Thierry Bronx", "T.Roy"]
        for name in names:
            sender.replace(name, "Me")
        return sender


    def get_receiver(self, message, sender, participants):
        receiver = participants[0] if sender == participants[1] else participants[1]
        receiver = self.encode_bytes_to_string(receiver)
        names = ["Thierry Bronx", "T.Roy"]
        for name in names:
            receiver.replace(name, "Me")
        return receiver

    def get_message(self, message: str, sender = ''):
        for sensitive_message in SENSITIVE_DATA:
            message = re.sub(rf"\b{re.escape(sensitive_message)}\b", "", message, flags=re.IGNORECASE)

        message = message.replace(sender,"")
        message = message.strip().replace(" .",".").replace("  ","")
        return self.encode_bytes_to_string(message)
                
    async def extract_data_from_json(self, file_path: Path):
        with open(file_path, "r") as file:
            data = json.load(file)
            participants = [participant["name"] for participant in data["participants"]]

            que_messages = []
            previous_message = None

            for message in data["messages"]:
                if len(participants) > 1:
                    sender = self.get_sender(message)
                    receiver = self.get_receiver(message, sender, participants)
                    content = (
                        message.get("content", "None")
                        if "content" in message
                        else "None"
                    )
                    timestamp_ms = message.get("timestamp_ms", 0)
                    timestamp_ms = datetime.fromtimestamp(timestamp_ms / 1000.0)
                    timestamp_ms = timestamp_ms.strftime("%Y-%m-%d %H:%M:%S")

                    if  previous_message and previous_message["sender"] == sender:
                        previous_message[
                            "message"
                        ] = f"{self.get_message(content, sender=sender)} \n {self.get_message(previous_message['message'], sender=sender)}"
                    else:
                        previous_message = {
                            "sender": sender,
                            "receiver": receiver,
                            "message":  self.get_message(content, sender=sender),
                            "timestamp_ms": timestamp_ms,
                        }
                        que_messages.append(previous_message)

            messages = sorted(
                que_messages, key=lambda x: x["timestamp_ms"], reverse=False
            )
            for message in messages:
                ALL_MESSAGES.append(message)
            return ALL_MESSAGES
            

    def main(self):
        for dir_name in self.inboxes_dir:
            dir_path = os.path.join(self.inbox_dir, dir_name)
            inbox_json_path = os.path.join(dir_path, "message_1.json")
            if os.path.exists(inbox_json_path):
                asyncio.run(self.extract_data_from_json(inbox_json_path))

        with open("data-test.json", "w") as outfile:
            json.dump(ALL_MESSAGES, outfile, indent=4)


if __name__ == "__main__":
    NOW = datetime.now().strftime("%H:%M:%S")
    make_json = MakeJson(
        INBOX_DIR,
    )
    make_json.main()
