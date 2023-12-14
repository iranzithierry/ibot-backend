import os
import shutil
import logging
import json
import re
import random
from pathlib import Path
from datetime import datetime


class FileManager:
    def __init__(
        self, inbox_dir, unknown_chat_dir, photos_path, videos_path, audios_path
    ):
        """
        Initializes the FileManager with the specified directories and paths.
        """
        self.inbox_dir = inbox_dir
        self.unknown_chat_dir = unknown_chat_dir
        self.photos_path = photos_path
        self.videos_path = videos_path
        self.audios_path = audios_path
        self.inboxs = os.listdir(inbox_dir)

    def move_file(
        self, destination_dir: Path, source_files_dir: Path, user_folder: str
    ):
        """
        Moves files from the source directory to the destination directory with a new filename.
        """
        try:
            if os.path.exists(source_files_dir):
                files_dir = os.listdir(source_files_dir)
                for file in files_dir:
                    file_path = os.path.join(source_files_dir, file)
                    extension = file.split(".")[-1]
                    remove_number = re.sub(r"_\d+$", "", user_folder)
                    random_number = "".join(
                        [str(random.randint(0, 9)) for _ in range(16)]
                    )
                    username_file_extension = (
                        f"{remove_number}-{random_number}.{extension}"
                    )
                    username_destination_path = os.path.join(
                        destination_dir, username_file_extension
                    )
                    try:
                        shutil.move(file_path, username_destination_path)
                        self.create_file(
                            file_name=f"{NOW}-Logs",
                            content=f"[MOVED] ({file.split('.')[0][0:25]}...).{extension} TO {username_destination_path.split('/')[-1]}",
                            append=True,
                        )
                    except FileExistsError as e:
                        break
            return "success"
        except OSError as oe:
            logging.error("OS Error: %s" % oe)
        except Exception as e:
            logging.exception(e)

    def delete_source_files_dir(self, source_files_dir: Path):
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

    def delete_directory(self, user_folder_dir: Path):
        """
        Removes a single folder.
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

    def move_directory(self, source_dir: Path, destination_dir: Path):
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

    def create_file(
        self,
        dir=os.getcwd(),
        file_name=f"{datetime.now()}.txt",
        content="",
        append=False,
    ):
        file_dir = os.path.join(dir, file_name)
        file_dir = Path(file_dir)
        file_dir.touch(exist_ok=True)
        if append:
            with open(file_dir, "+a") as file:
                file_data = file.write(f"""{content}\n""")
        else:
            with open(file_dir, "r") as file:
                file_data = file.read()
                if len(file_data) > 1:
                    with open(file_dir, "w") as file:
                        file_data = file.write(f"""{content}""")

    def create_media_directories(self):
        directories = [self.photos_path, self.videos_path, self.audios_path]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def classify_media_files(self):
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
                move_file = self.move_file(
                    media["destination"], media["source"], user_folder
                )
                if move_file == "success":
                    self.delete_source_files_dir(media["source"])
                else:
                    print(f"Error {move_file} On {media['source']}")

        print("Classify media files : DONE".upper())

    def move_uknown_chat_to_uknowns(self):
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
                if data["participants"][0]["name"] == "":
                    unknown_chat_array.append(f"{user_folder}")
        for file in unknown_chat_array:
            file_path = os.path.join(self.inbox_dir, file)
            shutil.move(file_path, self.unknown_chat_dir)
        print("move uknown chat to uknowns : DONE".upper())

    def renaming_folders(self):
        """
        Manages the user folders by renaming them.
        """
        folders = os.listdir(self.inbox_dir)
        for folder in folders:
            folder_dir = os.path.join(self.inbox_dir, folder)
            username = re.sub(r"_\d+$", "", folder)
            try:
                renamed_folder_dir = os.path.join(self.inbox_dir, username)
                os.rename(folder_dir, renamed_folder_dir)
                # print("renaming folders done".upper())
            except OSError as oe:
                continue


# Usage:
if __name__ == "__main__":
    NOW = datetime.now().strftime("%H:%M:%S")
    file_manager = FileManager(
        inbox_dir=Path("../data_classified/inbox/"),
        unknown_chat_dir="../data_classified/unknown_chat",
        photos_path=Path("../data_classified/photos"),
        videos_path=Path("../data_classified/videos"),
        audios_path=Path("../data_classified/audios"),
    )
    file_manager.create_media_directories()
    file_manager.classify_media_files()
    file_manager.move_uknown_chat_to_uknowns()
    file_manager.renaming_folders()
