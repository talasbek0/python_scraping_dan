import json
import time
import requests
from bs4 import BeautifulSoup
import datetime
import csv

start_time = time.time()
def get_data():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"labirint_{cur_time}.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(
            {
                "Назваение книги",
                 "Автор",
                 "Издательство",
                 "Цена со скидкой",
                 "Наличие на складе",

            }
        )
    headers ={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    url = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table"

    responce = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(responce.text, "lxml")
    print(f"Загрузка книг...")
    print("Загрузка авторов...")

    pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)

    books_data = []
    for page in range(1, pages_count + 1):
    # for page in range(1, 2):
        url = f"https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={page}"

        responce = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(responce.text, "lxml")

        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")
        for bi in books_items:
            book_data = bi.find_all("td")

            try:
                book_title = book_data[0].find("a").text.strip()
            except:
                book_title = "НЕТ НАЗВАНИЕ КНИГИ"
            try:
                book_author = book_data[1].text.strip()
            except:
                book_author = "НЕТ НАЗВАНИЕ АВТОРА"
            try:
                # book_publishin = book_data[2].text.strip()
                book_publishin = book_data[2].find_all("a")
                book_publishin = ":".join([bp.text for bp in book_publishin])
            except:
                book_publishin = "НЕТ ИЗДАТЕЛЬСТВa"
            try:
                book_new_price = book_data[3].find("div", class_="price").find("span").find("span").text.strip().replace(" ", ".")
            except:
                book_new_price = "Нет нового прайса"
            try:
                book_old_price = book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ".")
            except:
                book_old_price = "Скидка отсутсвует"
            try:
                book_status = book_data[-1].text.strip()
            except:
                book_status = "Нет статуса"
            # print(book_title)
            # print(book_author)
            # print(book_publishin)
            # print(book_new_price,f"СОМ")
            # print(book_old_price)
            # print(book_status)
            # print("#" * 10)

            books_data.append(
                {
                    "book_title": book_title,
                    "book_author": book_author,
                    "book_publishin": book_publishin,
                    "book_new_price": book_new_price,
                    "book_old_price": book_old_price,
                    "book_status": book_status
                }
            )
            with open(f"labirint_{cur_time}.csv", "a") as file:
                writer = csv.writer(file)

                writer.writerow(
                    {
                        book_title,
                        book_author,
                        book_publishin,
                        book_new_price,
                        book_old_price,
                        book_status
                    }
                )

        print(f"оброботана {page}/{pages_count}")
        time.sleep(1)

    with open(f"labirint_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(books_data,file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() -start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")

if _name_ == '_main_':
    main()           # 9-урок
