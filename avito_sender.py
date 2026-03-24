import asyncio
import random
import json
import os
from playwright.async_api import async_playwright
from avito_messages import get_random_message

# Конфигурация
CONFIG = {
    "proxy": None, # Прокси отключены по просьбе Админа
    "category_roof": "stroitelstvo/krovlya",
    "category_fences": "stroitelstvo/zabory_vorota",
    "delay_min": 60,  # 1 минута
    "delay_max": 300  # 5 минут
}

async def send_message_to_ads(city_url, city_name):
    async with async_playwright() as p:
        # Настройка прокси
        proxy = CONFIG.get("proxy")
        
        browser = await p.chromium.launch(headless=False)
        # Загружаем сохраненную сессию (создадим ее при первом входе)
        context = await browser.new_context(storage_state="auth_state.json" if os.path.exists("auth_state.json") else None)
        page = await context.new_page()
        
        print(f"[{city_name}] Переходим в категорию...")
        await page.goto(city_url)
        
        # Собираем ссылки на объявления (селекторы могут меняться, это пример)
        # Авито часто меняет классы, поэтому используем более общие селекторы
        ads = await page.locator('a[data-marker="item-title"]').all_links()
        
        for ad_url in ads[:5]: # Для теста берем первые 5
            print(f"Открываем объявление: {ad_url}")
            await page.goto(ad_url)
            
            # Ищем кнопку "Написать сообщение"
            btn_message = page.locator('button[data-marker="messenger-button"]')
            if await btn_message.is_visible():
                await btn_message.click()
                
                # Ждем поле ввода
                input_field = page.locator('textarea[data-marker="messenger-input"]')
                await input_field.wait_for(timeout=5000)
                
                # Генерируем текст
                text = get_random_message(city_name)
                print(f"Пишем: {text}")
                
                await input_field.fill(text)
                # await page.keyboard.press("Enter") # Раскомментировать для реальной отправки
                
                # Пауза между сообщениями (1-5 минут)
                wait_time = random.randint(CONFIG["delay_min"], CONFIG["delay_max"])
                print(f"Ждем {wait_time} сек перед следующим...")
                await asyncio.sleep(wait_time)
            else:
                print("Кнопка сообщения не найдена (возможно, только звонки)")
        
        await browser.close()

async def main():
    import avito_cities
    cities = avito_cities.load_cities_from_json("cities_list.json")
    for city in cities[:1]: # Тестируем на первом городе
        print(f"Запускаем рассылку по городу: {city['name']}")
        await send_message_to_ads(city['url'], city['name'])

if __name__ == "__main__":
    asyncio.run(main())
