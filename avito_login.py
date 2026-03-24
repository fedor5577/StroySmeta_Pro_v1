"""
Запусти этот скрипт ОДИН РАЗ чтобы войти в Авито вручную.
Сессия сохранится в auth_state.json и бот будет использовать её автоматически.
"""
import asyncio
from playwright.async_api import async_playwright

try:
    from playwright_stealth import stealth_async
    STEALTH = True
except ImportError:
    STEALTH = False

async def login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1440, "height": 900},
            locale="ru-RU",
        )
        page = await context.new_page()
        if STEALTH:
            await stealth_async(page)

        print("🌐 Открываю Авито...")
        await page.goto("https://www.avito.ru/", wait_until="domcontentloaded")

        print("")
        print("=" * 50)
        print("👤 ВОЙДИ В АККАУНТ АВИТО ВРУЧНУЮ В БРАУЗЕРЕ")
        print("   Нажми кнопку 'Войти', введи логин и пароль")
        print("   После входа вернись сюда и нажми ENTER")
        print("=" * 50)
        input("⏳ Нажми ENTER когда войдёшь в аккаунт...")

        # Сохраняем сессию
        await context.storage_state(path="auth_state.json")
        print("✅ Сессия сохранена в auth_state.json!")
        print("   Теперь запускай avito_sender_v2.py")

        await browser.close()

asyncio.run(login())
