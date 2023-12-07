import json
import csv
import os
json_file = os.path.join(os.getcwd(), "none_bytes_data.json")
with open(json_file, 'r') as file:
    json_data = file.read()

# Load JSON data
chat_data = json.loads(json_data)

# CSV file name
csv_file = "chat_data.csv"

# Write data to CSV file
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Request", "Response"])

    for idx in range(0, len(chat_data), 2):
        current_message = chat_data[idx]["message"]
        next_message = chat_data[idx + 1]["message"] if idx + 1 < len(chat_data) else ""

        writer.writerow([current_message, next_message])
