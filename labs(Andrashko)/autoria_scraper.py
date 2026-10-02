from playwright.sync_api import sync_playwright
import csv

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    print("Відкриваємо AUTO.RIA...")
    page.goto("https://auto.ria.com/uk/car/used/")

    print("Чекаємо завантаження даних (JavaScript)...")
    page.wait_for_selector(".ticket-item", timeout=10000)
    cars = page.query_selector_all(".ticket-item")
    print(f"Знайдено автомобілів на сторінці: {len(cars)}")

    scraped_data = []

    for car in cars:
        title_element = car.query_selector(".ticket-title a")
        title = title_element.text_content().strip() if title_element else "Невідомо"

        link = title_element.get_attribute("href") if title_element else "Немає посилання"

        price_element = car.query_selector(".price-ticket")
        price = price_element.text_content().strip() if price_element else "Не вказано"

        mileage_element = car.query_selector(".js-race")
        mileage = mileage_element.text_content().strip() if mileage_element else "Не вказано"

        scraped_data.append({
            "Назва": title,
            "Ціна": price,
            "Пробіг": mileage,
            "Посилання": link
        })

    print("Збір даних завершено. Зберігаємо у CSV...")

    with open("cars_data.csv", mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Назва", "Ціна", "Пробіг", "Посилання"])
        writer.writeheader()
        writer.writerows(scraped_data)

    print("Успішно збережено у файл cars_data.csv!")
    
    browser.close()

with sync_playwright() as playwright:
    run(playwright)