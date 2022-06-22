import asyncio
import base64
import os

import requests
import unicodedata
from dotenv import load_dotenv
from instagramy import InstagramUser

load_dotenv()
current_work_dir = os.path.dirname(os.path.realpath('__file__'))
session_id: str = os.environ.get("SESSION_ID") or ""


def get_input_session():
    while True:
        session_id = input("Input session_id: ")
        if len(session_id.strip()) != 0:
            break
        print("Session id cannot be empty")


def get_target_username() -> str:
    while True:
        instagram_username = input("Input target instagram username: ")
        if len(instagram_username.strip()) != 0:
            return instagram_username
        print("Username cannot be empty")


async def get_base64_from_url(image_url: str) -> str:
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode("utf-8")


async def get_instagram_details(instagram_username: str) -> dict:
    user = InstagramUser(instagram_username, sessionid=session_id, from_cache=True)
    return {
        "username": user.username,
        "name": unicodedata.normalize("NFKD", user.fullname).replace("\'", ""),
        "description": unicodedata.normalize("NFKD", user.biography).replace("\'", ""),
        "profile_pic": user.profile_picture_url,
        "pictures": user.posts_display_urls,
        }


def create_output_dir():
    if not os.path.isdir(os.path.join(current_work_dir, "outputs")):
        os.mkdir("outputs")


def print_result(data: dict):
    create_output_dir()
    username = data["username"]
    output_file_path = os.path.join(current_work_dir, "outputs", f"output_{username}.txt")
    with open(output_file_path, "w", encoding="utf_8") as f:
        f.write(str(data).replace('\'', '\"'))
    print(f"Success write output to: \"outputs/outputs_{username}.txt\"")


def get_next_query_confirmation() -> bool:
    while True:
        user_input = input("Get next username? (y/n)")
        if user_input == "Y" or user_input == "y":
            return True
        if user_input == "N" or user_input == "n":
            return False


async def main():
    if len(session_id) == 0:
        get_input_session()

    while True:
        instagram_username = get_target_username()
        data = await get_instagram_details(instagram_username)
        print_result(data)
        continue_query = get_next_query_confirmation()
        if not continue_query:
            break


if __name__ == '__main__':
    asyncio.run(main())
