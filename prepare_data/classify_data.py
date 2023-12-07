import os
import shutil
import logging
import json
import re
import random

class FileManager:
    def __init__(self, inbox_dir, unknown_chat_dir, photos_path, videos_path, audios_path):
        """
        Initializes the FileManager with the specified directories and paths.
        """
        self.inbox_dir = inbox_dir
        self.unknown_chat_dir = unknown_chat_dir
        self.photos_path = photos_path
        self.videos_path = videos_path
        self.audios_path = audios_path
        self.inboxs = os.listdir(inbox_dir)

    def move_user_files(self, destination_dir, source_files_dir, user_folder):
        """
        Moves files from the source directory to the destination directory with a new filename.
        """
        try:
            if os.path.exists(source_files_dir):
                files_dir = os.listdir(source_files_dir)
                for file in files_dir:
                    file_path = os.path.join(source_files_dir, file)
                    extension = file.split(".")[-1]
                    remove_number = re.sub(r'_\d+$', '', user_folder)
                    random_number = "".join([str(random.randint(0, 9)) for _ in range(16)])
                    username = f"{remove_number}-{random_number}.{extension}"
                    destination_path = os.path.join(destination_dir, username)
                    try:
                        shutil.move(file_path, destination_path)
                    except FileExistsError as e:
                        break
            return "success"
        except OSError as oe:
            logging.error("OS Error: %s" % oe)
        except Exception as e:
            logging.exception(e)

    def delete_user_files_dir(self, source_files_dir):
        """
        Deletes the entire directory of user files.
        """
        try:
            if os.path.exists(source_files_dir):
                os.chmod(source_files_dir, 0o777)
                shutil.rmtree(source_files_dir)
            return "success"
        except PermissionError as pe:
            logging.error(f"Permission error: {pe}")
            return "permission_error"
        except Exception as e:
            logging.exception(e)
            return "error"

    def remove_single_folder(self, user_folder_dir):
        """
        Removes a single user folder.
        """
        try:
            if os.path.exists(user_folder_dir):
                os.chmod(user_folder_dir, 0o777)
                shutil.rmtree(user_folder_dir)
            return "success"
        except PermissionError as pe:
            logging.error(f"Permission error: {pe}")
            return "permission_error"
        except Exception as e:
            logging.exception(e)
            return "error"

    def move_single_folder(self, source_dir, destination_dir):
        """
        Function yogu cutting one dir to onother
        Moves a single folder from the source to the destination directory.
        """
        try:
            if os.path.exists(source_dir):
                shutil.move(source_dir, destination_dir)
            return "success"
        except OSError as oe:
            logging.error("OS Error: %s" % oe)
        except Exception as e:
            logging.exception(e)

    def manage_user_files(self):
        """
        Gucamo ibice ama file ya video, audiom and photos muri folder imwe.
        Manages user files by moving them to appropriate directories and deleting the source directories.
        """
        for user_folder in self.inboxs:
            user_folder_path = os.path.join(self.inbox_dir, user_folder)
            user_photos_path = os.path.join(user_folder_path, "photos")
            user_audios_path = os.path.join(user_folder_path, "audio")
            user_videos_path = os.path.join(user_folder_path, "videos")
            medias_array = [
                {"destination": self.audios_path, "source": user_audios_path},
                {"destination": self.videos_path, "source": user_videos_path},
                {"destination": self.photos_path, "source": user_photos_path},
            ]
            for media in medias_array:
                move_files_msg = self.move_user_files(media['destination'], media['source'], user_folder)
                if move_files_msg == "success":
                    self.delete_user_files_dir(media['source'])
                else:
                    print(f"Error {move_files_msg} On {media['source']}")

        print("manage_user_files : DONE")

    def check_unknown_chat(self):
        """
        Nimba muri messages umwe adafite izina means izi unknown need to be removed.
        Checks for unknown chat folders and moves them to the specified unknown chat directory.
        """
        unknown_chat_array = []
        for user_folder in self.inboxs:
            user_folder_path = os.path.join(self.inbox_dir, user_folder)
            json_file_path = os.path.join(user_folder_path, "message_1.json")
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)
                if data['participants'][0]['name'] == '':
                    unknown_chat_array.append(f"{user_folder}")
        for file in unknown_chat_array:
            file_path = os.path.join(self.inbox_dir, file)
            shutil.move(file_path, self.unknown_chat_dir)
        print("check_unknown_chat : DONE")

    def manage_unknown_chat(self):
        """
        Manages unknown chat folders by categorizing them as single or multi chat and taking appropriate actions.
        nimba nta message zihari zimwe zirasibwa izindi zijyanwe muri inbox
        """
        unknown_chats = os.listdir(self.unknown_chat_dir)
        single_chat = []
        multi_chat = []
        for folder in unknown_chats:
            unknown_chat_path = os.path.join(self.unknown_chat_dir, folder)
            json_file_path = os.path.join(unknown_chat_path, "message_1.json")
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)
                messages = data['messages']
                if len(messages) <= 10:
                    single_chat.append(unknown_chat_path)
                else:
                    multi_chat.append(unknown_chat_path)

        for participant in single_chat:
            self.remove_single_folder(participant)

        for participant in multi_chat:
            self.move_single_folder(participant, self.inbox_dir)
        print("manage_unknown_chat : DONE")

    def manage_folders(self):
        """
        Manages the user folders by renaming them.
        """
        folders = os.listdir(self.inbox_dir)
        for folder in folders:
            folder_dir = os.path.join(self.inbox_dir, folder)
            username = re.sub(r'_\d+$', '', folder)
            try:
                renamed_folder_dir = os.path.join(self.inbox_dir, username)
                os.rename(folder_dir, renamed_folder_dir)
            except OSError as oe:
                continue


# Usage:
if __name__ == "__main__":
    file_manager = FileManager(
        inbox_dir="messages/inbox/", 
        unknown_chat_dir="messages/unknown_chat",
        photos_path="messages/photos", 
        videos_path="messages/videos", 
        audios_path="messages/audios"
    )
    # file_manager.manage_user_files()
    # file_manager.check_unknown_chat()
    file_manager.manage_unknown_chat()
    # file_manager.manage_folders()
