import requests
from bs4 import BeautifulSoup
from config import token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    await message.reply("Привет!\nНапиши мне название монеты и увидишь о ней информацию!")


@dp.message_handler()
async def get_coin_info(message: types.Message):
    try:
        response = requests.get("https://coinmarketcap.com/currencies/" + message["text"])
        soup = BeautifulSoup(response.text, "html.parser")

        full_coin_name = soup.find("span", class_="sc-169cagi-0").text
        short_coin_name = soup.find("small", class_="nameSymbol").text
        rank = soup.find("div", "namePill").text.split()[1]
        price = soup.find("div", class_="priceValue").text
        market_cap = soup.find("div", class_="statsItemRight").find(class_="statsValue").text
        volume_24_hours = soup.find_all("div", class_="statsItemRight")[2].next.text

        coin_category_tag = ""
        fonds_count = 0
        for card in soup.find_all("div", class_="sc-1prm8qw-0 eRkGuy"):
            if "Category" in card.text:
                coin_category_tag = card.find("div", class_="sc-10up5z1-2 iEatlr")

        for fond in coin_category_tag:
            if fond.text.endswith("Portfolio"):
                fonds_count += 1

        await message.reply(f"Название монеты: {full_coin_name} / {short_coin_name}\n" \
                            f"Ранг: {rank}\n" \
                            f"Цена: {price}\n" \
                            f"Капитализация: {market_cap}\n" \
                            f"Объем: {volume_24_hours}\n" \
                            f"Кол-во фондов: {fonds_count}")

    except:
        await message.reply("Неверное название монеты!")


if __name__ == '__main__':
    executor.start_polling(dp)
