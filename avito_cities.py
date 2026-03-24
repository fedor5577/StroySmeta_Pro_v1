import json

# Список городов России с населением более 100 000 человек (основные)
# Данные примерные, для полноценной работы можно расширить через API
cities_100kplus = [
    {"city": "Москва", "region": "Москва"},
    {"city": "Санкт-Петербург", "region": "Санкт-Петербург"},
    {"city": "Новосибирск", "region": "Новосибирская область"},
    {"city": "Екатеринбург", "region": "Свердловская область"},
    {"city": "Казань", "region": "Татарстан"},
    {"city": "Нижний Новгород", "region": "Нижегородская область"},
    {"city": "Челябинск", "region": "Челябинская область"},
    {"city": "Самара", "region": "Самарская область"},
    {"city": "Омск", "region": "Омская область"},
    {"city": "Ростов-на-Дону", "region": "Ростовская область"},
    {"city": "Уфа", "region": "Башкортостан"},
    {"city": "Красноярск", "region": "Красноярский край"},
    {"city": "Воронеж", "region": "Воронежская область"},
    {"city": "Пермь", "region": "Пермский край"},
    {"city": "Волгоград", "region": "Волгоградская область"},
    {"city": "Краснодар", "region": "Краснодарский край"},
    {"city": "Тюмень", "region": "Тюменская область"},
    {"city": "Саратов", "region": "Саратовская область"},
    {"city": "Тольятти", "region": "Самарская область"},
    {"city": "Ижевск", "region": "Удмуртия"},
    {"city": "Барнаул", "region": "Алтайский край"},
    {"city": "Ульяновск", "region": "Ульяновская область"},
    {"city": "Иркутск", "region": "Иркутская область"},
    {"city": "Хабаровск", "region": "Хабаровский край"},
    {"city": "Махачкала", "region": "Дагестан"},
    {"city": "Владивосток", "region": "Приморский край"},
    {"city": "Ярославль", "region": "Ярославская область"},
    {"city": "Оренбург", "region": "Оренбургская область"},
    {"city": "Томск", "region": "Томская область"},
    {"city": "Кемерово", "region": "Кемеровская область"},
    {"city": "Новокузнецк", "region": "Кемеровская область"},
    {"city": "Рязань", "region": "Рязанская область"},
    {"city": "Набережные Челны", "region": "Татарстан"},
    {"city": "Астрахань", "region": "Астраханская область"},
    {"city": "Киров", "region": "Кировская область"},
    {"city": "Пенза", "region": "Пензенская область"},
    {"city": "Севастополь", "region": "Севастополь"},
    {"city": "Липецк", "region": "Липецкая область"},
    {"city": "Балашиха", "region": "Московская область"},
    {"city": "Чебоксары", "region": "Чувашия"},
    {"city": "Калининград", "region": "Калининградская область"},
    {"city": "Тула", "region": "Тульская область"},
    {"city": "Ставрополь", "region": "Ставропольский край"},
    {"city": "Курск", "region": "Курская область"},
    {"city": "Улан-Удэ", "region": "Бурятия"},
    {"city": "Сочи", "region": "Краснодарский край"},
    {"city": "Тверь", "region": "Тверская область"},
    {"city": "Магнитогорск", "region": "Челябинская область"},
    {"city": "Иваново", "region": "Ивановская область"},
    {"city": "Брянск", "region": "Брянская область"},
    {"city": "Белгород", "region": "Белгородская область"},
    {"city": "Сургут", "region": "Ханты-Мансийский АО"},
    {"city": "Владимир", "region": "Владимирская область"},
    {"city": "Чита", "region": "Забайкальский край"},
    {"city": "Архангельск", "region": "Архангельская область"},
    {"city": "Нижний Тагил", "region": "Свердловская область"},
    {"city": "Смоленск", "region": "Смоленская область"},
    {"city": "Калуга", "region": "Калужская область"},
    {"city": "Саранск", "region": "Мордовия"},
    {"city": "Череповец", "region": "Вологодская область"},
    {"city": "Курган", "region": "Курганская область"},
    {"city": "Орёл", "region": "Орловская область"},
    {"city": "Вологда", "region": "Вологодская область"},
    {"city": "Подольск", "region": "Московская область"},
    {"city": "Грозный", "region": "Чечня"},
    {"city": "Мурманск", "region": "Мурманская область"},
    {"city": "Тамбов", "region": "Тамбовская область"},
    {"city": "Петрозаводск", "region": "Карелия"},
    {"city": "Стерлитамак", "region": "Башкортостан"},
    {"city": "Нижневартовск", "region": "Ханты-Мансийский АО"},
    {"city": "Кострома", "region": "Костромская область"},
    {"city": "Новороссийск", "region": "Краснодарский край"},
    {"city": "Йошкар-Ола", "region": "Марий Эл"},
    {"city": "Химки", "region": "Московская область"},
    {"city": "Таганрог", "region": "Ростовская область"}
]

# Функция для генерации ссылок Авито для поиска услуг
def generate_avito_links(cities, category_slug="predlozheniya_uslug"):
    # Примерные слаги категорий: 
    # Кровля: stroitelstvo/krovlya
    # Заборы: stroitelstvo/zabory_vorota
    base_url = "https://www.avito.ru"
    
    links = []
    for item in cities:
        # В Авито города обычно пишутся латиницей в URL, 
        # но для упрощения на старте можно использовать поиск по названию
        # или составить карту соответствия.
        links.append({
            "city": item["city"],
            "url_roof": f"{base_url}/{item['city'].lower()}/predlozheniya_uslug/stroitelstvo/krovlya",
            "url_fences": f"{base_url}/{item['city'].lower()}/predlozheniya_uslug/stroitelstvo/zabory_vorota"
        })
    return links

def load_cities_from_json(filepath="cities_list.json"):
    """Загружает список городов из JSON-файла. 
    Если файл не найден — возвращает встроенный список cities_100kplus."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Нормализуем: поддерживаем и {"city": ..., "region": ...} и {"name": ..., "url": ...}
        result = []
        for item in data:
            city_name = item.get("city") or item.get("name", "")
            region = item.get("region", "")
            url = item.get("url", "")
            result.append({"city": city_name, "name": city_name, "region": region, "url": url})
        return result
    except FileNotFoundError:
        print(f"[avito_cities] Файл {filepath} не найден, используем встроенный список.")
        return [{"city": c["city"], "name": c["city"], "region": c["region"], "url": ""} for c in cities_100kplus]

if __name__ == "__main__":
    with open("cities_list.json", "w", encoding="utf-8") as f:
        json.dump(cities_100kplus, f, ensure_ascii=False, indent=2)
    print(f"Список из {len(cities_100kplus)} городов сохранен в cities_list.json")
