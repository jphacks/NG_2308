import httpx
import os
import asyncio
import datetime
import json
import csv

from dotenv import load_dotenv
from pathlib import Path

# カレントディレクトリにある.envをロード
dotenv_path = "{}/.env".format(os.getcwd())
load_dotenv(dotenv_path=dotenv_path)

# ログファイルに追記
def append_log(timestamp: int, search_word: str, content: str, is_same_topic: bool):

    # 該当ディレクトリ・ファイルの存在確認, 新規作成
    directory_path = Path("{}/var".format(os.getcwd()))
    file_path = Path("{}/var/judge.csv".format(os.getcwd()))
    if not directory_path.exists(): directory_path.mkdir()
    if not file_path.exists(): file_path.touch()

    # 全角コンマ「、」に置換
    search_word = search_word.replace(",", "、")
    content = content.replace(",", "、")

    # csvファイルをロード
    with open(file_path, mode='a') as file:
        writer = csv.writer(file)
        # 行を追記
        writer.writerow([timestamp, search_word, content, is_same_topic])


# コンテンツと時刻情報をLLMに送信
async def judge(client_uuid: str, search_word: str, content: str):

    # POSTリクエストでLLMと非同期通信
    async with httpx.AsyncClient() as client:
        llm_url = "{}/on_action".format(os.getenv("LLM_SERVER"))
        post_data = {
            "client_uuid": client_uuid,
            "search_word": search_word,
            "page_content": content,
        }
        print(llm_url, post_data)
        response = await client.post(llm_url, json=post_data, timeout=120.0)

    # ログファイルに追記
    current_datetime = datetime.datetime.now()
    timestamp = int(current_datetime.timestamp())

    res_content = json.loads(response.content)

    append_log(timestamp, search_word, content, res_content["is_same_topic"])

    # POSTリクエストで受け取ったUUIDを返す
    return res_content["client_uuid"]

if __name__ == "__main__":
    asyncio.run(judge("", "hello world", "中身です"))
