# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env') # 環境変数をおいたディレクトリで指定
load_dotenv(dotenv_path)

discordAPI = os.environ.get("DISCORD_API_TOKEN")