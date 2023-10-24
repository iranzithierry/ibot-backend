import json
import Levenshtein
import random
import click

with open("data.json", "r", encoding="utf-8") as file:
    chat_data = json.load(file)


# Extract and clean message text
def calculate_similarity(query, message):
    return Levenshtein.ratio(query.lower(), message.lower())


def get_bot_response(query):
    matching_responses = []  # Store potential matching responses
    best_similarity = 0.0

    # Iterate through chat data to find matching sender messages
    for idx, message in enumerate(chat_data):
        # if message["receiver"] == "T.Roy.":
            similarity = calculate_similarity(query, message["message"])
            if similarity > 0.7 and idx < len(chat_data) - 1:
                # Check if the next message is from the receiver
                next_message = chat_data[idx + 1]
                if next_message["receiver"] == message["sender"]:
                    matching_responses.append(next_message["message"])
                    best_similarity = similarity

    # If there are matching responses, randomly select one
    if matching_responses:
        print(matching_responses)
        bot_response = random.choice(matching_responses)
    else:
        bot_response = "Bot couldn't find a matching response."

    return (
        bot_response.replace("bsxr", "***")
        .replace("gxr", "***")
        .replace("gswer", "***")
        .replace("gswr","***")
        .replace("knyk","***"),
        best_similarity,
    )


# Example usage:
while True:
    user_query = input(click.style("You 😎 >","red", bold=True))
    response, similarity = get_bot_response(user_query)

    if response:
        print(f"Bot 🤖: {response} (Similarity: {similarity:.2f})")
