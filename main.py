from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import requests
from bs4 import BeautifulSoup
from pyrogram.types import ChatPermissions
import subprocess
import time
from time import sleep
import random
import wikipediaapi #pip install Wikipedia-API

app = Client("my_account")

@app.on_message(filters.command("type", prefixes=".") & filters.me)
def type(_, msg):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = "" # to be printed
    typing_symbol = "▒"
    while(tbp != orig_text):
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.01) # 50 ms

            tbp = tbp + text[0]
            text = text[1:]

            msg.edit(tbp)
            sleep(0.01)

        except FloodWait as e:
            sleep(e.x)

@app.on_message(filters.command("cm", prefixes=".") & filters.me)
def commands(_, msg):
    to_send = msg.text.split(None, 1)
    result = subprocess.run(to_send[1], shell = True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            encoding='utf-8')
    if result.returncode == 0:
        try:
            msg.edit(f"`{result.stdout}`", parse_mode="MARKDOWN")
        except:
            msg.edit(f"`Команда завершена удачно`", parse_mode="MARKDOWN")
    else:
        msg.edit(f"`Я не могу выполнить эту команду`", parse_mode="MARKDOWN")

@app.on_message(filters.command("site", prefixes=".") & filters.me)
def screenshot_site(_, msg):
    to_send = msg.text.split(None, 1)
    msg.delete()
    app.send_photo(chat_id=msg.chat.id, photo="https://mini.s-shot.ru/1366x768/JPEG/1366/Z100/?" + to_send[1])

@app.on_message(filters.command("search", prefixes=".") & filters.me)
def search_google(_, msg):
    user_agent = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    to_send = msg.text.split(None, 1) #Запрашиваем у юзера, что он хочет найти
    url = requests.get('https://www.google.com/search?q=' + to_send[1], headers=user_agent) #Делаем запрос
    soup = BeautifulSoup(url.text, features="lxml") #Получаем запрос
    r = soup.find_all("div", class_="yuRUbf") #Выводи весь тег div class="r"
    results_news = []
    for s in r:
        link = s.find('a').get('href') #Ищем ссылки по тегу <a href="example.com"
        title = s.find("h3") #Ищем описание ссылки по тегу <h3 class="LC20lb DKV0Md"
        title = title.get_text() #Вытаскиваем описание
        results = f"[{title}]({link})"
        results_news.append(results)
        result = "\n".join(results_news)

    msg.edit(f'Результаты по запросу: `"{to_send[1]}"`\n\n{result}', parse_mode="MARKDOWN")

@app.on_message(filters.command("wiki", prefixes=".") & filters.me)
def wiki(_, msg):
    try:
        wiki_wiki = wikipediaapi.Wikipedia(
            language='ru',
            extract_format=wikipediaapi.ExtractFormat.WIKI)
        page_py = wiki_wiki.page(msg.text.split(None, 1))
        msg.edit(f"`{page_py.summary}`", parse_mode="MARKDOWN")

    except:
        msg.edit("По вашему запросу ничего не найдено")

app.run()
