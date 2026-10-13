from playwright.sync_api import sync_playwright
import csv

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    print("Відкриваємо AUTO.RIA...")
    page.goto("https://auto.ria.com/uk/car/used/")
    page.wait_for_timeout(3000)

    scraped_data = []
    current_page = 1

    while current_page >= 1:
        page.wait_for_selector(".ticket-item", timeout=10000)
        cars = page.query_selector_all(".ticket-item")
        print(f"Сторінка {current_page}: знайдено {len(cars)} авто")

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

        next_button = page.locator(".page-link.js-next")
        if next_button.count() > 0 and next_button.is_visible():
            next_button.click()
            page.wait_for_timeout(3000)
            current_page += 1
        else:
            print("Остання сторінка, наступних сторінок немає.")
            break

    print("Збір даних завершено. Зберігаємо у CSV...")

    with open("cars_data.csv", mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Назва", "Ціна", "Пробіг", "Посилання"])
        writer.writeheader()
        writer.writerows(scraped_data)

    print("Успішно збережено у файл cars_data.csv!")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)