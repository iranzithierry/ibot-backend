import json


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


with open("data.json", "r") as file:
    json_data = file.read()

# Load JSON data
data = []
chat_data = json.loads(json_data)
for chat in chat_data:
    new = {
        "sender": encode_bytes_to_string(chat["sender"]),
        "receiver": encode_bytes_to_string(chat["receiver"]),
        "message": encode_bytes_to_string(chat["message"]),
    }
    data.append(new)


with open("none_bytes_data.json", "a") as file:
    json.dump(data, file, indent=4)
