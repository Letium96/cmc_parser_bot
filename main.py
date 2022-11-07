import requests
from bs4 import BeautifulSoup


def get_coin_info(coin):
    try:
        response = requests.get("https://coinmarketcap.com/currencies/" + coin)
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

        return f"Название монеты: {full_coin_name} / {short_coin_name}\n" \
               f"Ранг: {rank}\n" \
               f"Цена: {price}\n" \
               f"Капитализация: {market_cap}\n" \
               f"Объем: {volume_24_hours}\n" \
               f"Кол-во фондов: {fonds_count}" \

    except Exception as ex:
        print(ex)
        return "Неверное название монеты!"


def main():
    coin_name = input("Введите название монеты: ")
    print(get_coin_info(coin_name))


if __name__ == '__main__':
    main()
