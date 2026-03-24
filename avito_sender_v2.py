import asyncio
import random
import json
import os
from playwright.async_api import async_playwright
from avito_messages import get_random_message

# pip install playwright-stealth
try:
    from playwright_stealth import stealth_async
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False
    print("⚠️  playwright-stealth не установлен. Запусти: pip install playwright-stealth")

# =====================================================
# КОНФИГУРАЦИЯ
# =====================================================
CONFIG = {
    "delay_min": 45,        # мин. пауза между сообщениями (сек)
    "delay_max": 120,       # макс. пауза между сообщениями (сек)
    "city_delay_min": 180,  # пауза между городами (3 мин)
    "city_delay_max": 360,  # пауза между городами (6 мин)
    "ads_per_city": 7,      # сколько объявлений обрабатывать на город
    "headless": False,      # False = видим браузер, True = скрытый режим

    # Прокси — заполни если есть (формат: http://login:pass@host:port)
    # Мобильные прокси лучше всего: mobileproxies.ru, proxy6.net и т.д.
    "proxy": None,
    # Пример: "proxy": "http://user123:pass456@gate.mobileproxies.ru:9999"
}

# =====================================================
# СПИСОК ГОРОДОВ С РЕАЛЬНЫМИ URL АВИТО
# Формат: (название_для_сообщений, url_поиска)
# URL берём прямо с Авито — заходим на нужную страницу и копируем адрес
# =====================================================
CITIES = [
    ("Краснодар",       "https://www.avito.ru/krasnodarskiy_kray/predlozheniya_uslug/stroitelstvo-ASgBAgICAUSYC6Cf8QI?cd=1&localPriority=0&q=кровельные+работы"),
    ("Москва",          "https://www.avito.ru/moskva/predlozheniya_uslug/stroitelstvo-ASgBAgICAUSYC6Cf8QI?cd=1&localPriority=0&q=кровельные+работы"),
    ("Санкт-Петербург", "https://www.avito.ru/sankt-peterburg/predlozheniya_uslug/stroitelstvo-ASgBAgICAUSYC6Cf8QI?cd=1&localPriority=0&q=кровельные+работы"),
    ("Воронеж",         "https://www.avito.ru/voronezh/predlozheniya_uslug/stroitelstvo-ASgBAgICAUSYC6Cf8QI?cd=1&localPriority=0&q=кровельные+работы"),
    ("Ростов-на-Дону",  "https://www.avito.ru/rostov-na-donu/predlozheniya_uslug/stroitelstvo-ASgBAgICAUSYC6Cf8QI?cd=1&localPriority=0&q=кровельные+работы"),
    ("Самара",          "https://www.avito.ru/samara/predlozheniya_uslug/stroitelstvo-ASgBAgICAUSYC6Cf8QI?cd=1&localPriority=0&q=кровельные+работы"),
    ("Казань",          "https://www.avito.ru/kazan/predlozheniya_uslug/stroitelstvo-ASgBAgICAUSYC6Cf8QI?cd=1&localPriority=0&q=кровельные+работы"),
    ("Нижний Новгород", "https://www.avito.ru/nizhniy_novgorod/predlozheniya_uslug/stroitelstvo-ASgBAgICAUSYC6Cf8QI?cd=1&localPriority=0&q=кровельные+работы"),
    ("Екатеринбург",    "https://www.avito.ru/ekaterinburg/predlozheniya_uslug/stroitelstvo-ASgBAgICAUSYC6Cf8QI?cd=1&localPriority=0&q=кровельные+работы"),
    ("Рязань",          "https://www.avito.ru/ryazan/predlozheniya_uslug/stroitelstvo-ASgBAgICAUSYC6Cf8QI?cd=1&localPriority=0&q=кровельные+работы"),
    ("Подольск",        "https://www.avito.ru/podolsk/predlozheniya_uslug/stroitelstvo-ASgBAgICAUSYC6Cf8QI?cd=1&localPriority=0&q=кровельные+работы"),
    ("Липецк",          "https://www.avito.ru/lipetsk/predlozheniya_uslug/stroitelstvo-ASgBAgICAUSYC6Cf8QI?cd=1&localPriority=0&q=кровельные+работы"),
]

# =====================================================
# ПУЛЫ USER AGENT для ротации (анти-бан)
# =====================================================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

VIEWPORTS = [
    {"width": 1366, "height": 768},
    {"width": 1440, "height": 900},
    {"width": 1920, "height": 1080},
    {"width": 1280, "height": 800},
    {"width": 1600, "height": 900},
]


async def send_message_to_ads(city_url, city_name):
    """Обрабатывает один город: заходит на страницу поиска, находит объявления и пишет мастерам."""
    proxy_config = None
    if CONFIG.get("proxy"):
        proxy_config = {"server": CONFIG["proxy"]}

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=CONFIG["headless"],
            proxy=proxy_config,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ]
        )

        user_agent = random.choice(USER_AGENTS)
        viewport = random.choice(VIEWPORTS)

        context = await browser.new_context(
            user_agent=user_agent,
            viewport=viewport,
            locale="ru-RU",
            timezone_id="Europe/Moscow",
            storage_state="auth_state.json" if os.path.exists("auth_state.json") else None,
            extra_http_headers={
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            }
        )

        # Скрываем следы автоматизации
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru']});
        """)

        page = await context.new_page()

        # Применяем stealth-патч если доступен
        if STEALTH_AVAILABLE:
            await stealth_async(page)
            print("🥷 Stealth режим активен")

        print(f"\n{'='*50}")
        print(f"🏙️  Город: {city_name}")
        print(f"🌐  UA: {user_agent[:60]}...")
        print(f"{'='*50}")

        try:
            await page.goto(city_url, wait_until="domcontentloaded", timeout=60000)

            # Небольшая пауза чтобы загрузился динамический контент
            await page.wait_for_timeout(random.randint(2000, 4000))

            # Собираем ссылки на объявления
            ads = await page.evaluate("""
                () => Array.from(
                    document.querySelectorAll('div[data-marker^="item"] a[data-marker="item-title"]')
                ).map(a => a.href).filter(h => h && h.startsWith('https'))
            """)

            print(f"📋 Найдено объявлений: {len(ads)}")

            if not ads:
                print("⚠️  Объявления не найдены. Возможно, структура страницы изменилась или нужна авторизация.")
                await browser.close()
                return 0

            sent_count = 0
            for ad_url in ads[:CONFIG["ads_per_city"]]:
                try:
                    print(f"\n📌 Открываем: {ad_url}")
                    new_page = await context.new_page()
                    await new_page.goto(ad_url, wait_until="domcontentloaded", timeout=40000)
                    await new_page.wait_for_timeout(random.randint(2000, 4000))

                    # Ищем кнопку "Написать" — пробуем несколько селекторов
                    # Авито периодически меняет data-marker
                    MSG_BTN_SELECTORS = [
                        'button[data-marker="messenger-button"]',
                        'button[data-marker="contact-bar/write"]',
                        'button[data-marker="item-contact/messenger"]',
                        'button:has-text("Написать")',
                        'a:has-text("Написать")',
                        '[class*="messenger-button"]',
                        '[class*="write-button"]',
                    ]

                    btn = None
                    btn_selector_used = None
                    for sel in MSG_BTN_SELECTORS:
                        try:
                            candidate = new_page.locator(sel).first
                            if await candidate.is_visible(timeout=2000):
                                btn = candidate
                                btn_selector_used = sel
                                break
                        except:
                            continue

                    if btn:
                        print(f"🔍 Кнопка найдена: {btn_selector_used}")
                        # Двигаем мышь к кнопке как человек (случайное смещение)
                        box = await btn.bounding_box()
                        if box:
                            x = box["x"] + box["width"] / 2 + random.randint(-5, 5)
                            y = box["y"] + box["height"] / 2 + random.randint(-3, 3)
                            await new_page.mouse.move(x, y, steps=random.randint(5, 15))
                            await new_page.wait_for_timeout(random.randint(200, 600))
                        await btn.click()
                        await new_page.wait_for_timeout(random.randint(1500, 2500))

                        # Вводим текст — тоже пробуем несколько селекторов
                        TEXTAREA_SELECTORS = [
                            'textarea[data-marker="messenger-input"]',
                            'textarea[data-marker="message-input"]',
                            'textarea[placeholder*="сообщен"]',
                            'textarea[placeholder*="Напишите"]',
                            'div[contenteditable="true"]',
                        ]
                        textarea = None
                        for sel in TEXTAREA_SELECTORS:
                            try:
                                candidate = new_page.locator(sel).first
                                if await candidate.is_visible(timeout=2000):
                                    textarea = candidate
                                    break
                            except:
                                continue

                        if textarea:
                            text = get_random_message(city_name)
                            await textarea.click()
                            await new_page.keyboard.type(text, delay=random.randint(30, 80))
                            await new_page.wait_for_timeout(random.randint(800, 1500))

                            # Отправляем
                            SUBMIT_SELECTORS = [
                                'button[data-marker="messenger-submit"]',
                                'button[data-marker="message-submit"]',
                                'button:has-text("Отправить")',
                                '[class*="submit"]',
                            ]
                            submitted = False
                            for sel in SUBMIT_SELECTORS:
                                try:
                                    submit_btn = new_page.locator(sel).first
                                    if await submit_btn.is_visible(timeout=2000):
                                        await submit_btn.click()
                                        print(f"✅ Отправили: «{text[:50]}...»")
                                        sent_count += 1
                                        submitted = True
                                        break
                                except:
                                    continue
                            if not submitted:
                                # Пробуем Enter как запасной вариант
                                await new_page.keyboard.press("Enter")
                                print(f"✅ Отправили через Enter: «{text[:50]}...»")
                                sent_count += 1
                        else:
                            print("❌ Поле ввода не открылось")
                    else:
                        # Распечатаем все data-marker кнопки на странице для диагностики
                        markers = await new_page.evaluate("""
                            () => Array.from(document.querySelectorAll('button[data-marker], a[data-marker]'))
                                      .map(el => el.getAttribute('data-marker') + ' | ' + el.innerText.trim().slice(0,30))
                                      .slice(0, 20)
                        """)
                        print(f"⏭️  Кнопка сообщения не найдена. Кнопки на странице:")
                        for m in markers:
                            print(f"   → {m}")

                    await new_page.close()

                    # Пауза между объявлениями (анти-бан)
                    wait = random.randint(CONFIG["delay_min"], CONFIG["delay_max"])
                    print(f"⏳ Пауза {wait} сек...")
                    await asyncio.sleep(wait)

                except Exception as e:
                    print(f"⚠️  Ошибка на объявлении: {e}")
                    try:
                        await new_page.close()
                    except:
                        pass
                    continue

        except Exception as e:
            print(f"❌ Ошибка при обработке города {city_name}: {e}")

        finally:
            await browser.close()

    return sent_count


async def main():
    # Если есть файл с городами — берём оттуда, иначе встроенный список
    cities_to_run = CITIES

    if os.path.exists("my_cities.json"):
        with open("my_cities.json", "r", encoding="utf-8") as f:
            custom = json.load(f)
        cities_to_run = [(c["name"], c["url"]) for c in custom]
        print(f"📂 Загружен кастомный список: {len(cities_to_run)} городов")
    else:
        print(f"📋 Используем встроенный список: {len(cities_to_run)} городов")

    total_sent = 0
    for i, (city_name, city_url) in enumerate(cities_to_run):
        sent = await send_message_to_ads(city_url, city_name)
        total_sent += sent
        print(f"\n📊 Итого отправлено по {city_name}: {sent}")

        # Пауза между городами (кроме последнего)
        if i < len(cities_to_run) - 1:
            pause = random.randint(CONFIG["city_delay_min"], CONFIG["city_delay_max"])
            print(f"\n🏙️  Следующий город через {pause} сек ({pause//60} мин)...")
            await asyncio.sleep(pause)

    print(f"\n{'='*50}")
    print(f"🎯 ИТОГО отправлено сообщений: {total_sent}")
    print(f"{'='*50}")


if __name__ == "__main__":
    asyncio.run(main())
