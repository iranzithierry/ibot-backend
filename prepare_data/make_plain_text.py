import json
import csv
import os
json_file = os.path.join(os.getcwd(), "data-beta[,].json")
print(json_file)
with open(json_file, 'r') as file:
    json_data = file.read()

# Load JSON data
chat_data = json.loads(json_data)

writer = open("data-beta.txt","a+")

for idx in range(0, len(chat_data)):
    current_message = chat_data[idx]["message"]

    if chat_data[idx]["sender"] == "T.Roy":
        sender =  "BOT"
    else:
        sender = "USER"

    if idx + 1 < len(chat_data) and chat_data[idx]["receiver"] == "T.Roy":
        receiver =  "BOT"
    else:
        receiver = "USER"
        
    writer.write(f"[{sender}]: {current_message}\n")

