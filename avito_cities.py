import json

# Список городов России с населением более 100 000 человек
# slug — это транслитерация для URL Авито (avito.ru/{slug}/...)
cities_100kplus = [
    {"city": "Москва",             "region": "Москва",                    "slug": "moskva"},
    {"city": "Санкт-Петербург",    "region": "Санкт-Петербург",           "slug": "sankt-peterburg"},
    {"city": "Новосибирск",        "region": "Новосибирская область",      "slug": "novosibirsk"},
    {"city": "Екатеринбург",       "region": "Свердловская область",       "slug": "ekaterinburg"},
    {"city": "Казань",             "region": "Татарстан",                  "slug": "kazan"},
    {"city": "Нижний Новгород",    "region": "Нижегородская область",      "slug": "nizhniy_novgorod"},
    {"city": "Челябинск",          "region": "Челябинская область",        "slug": "chelyabinsk"},
    {"city": "Самара",             "region": "Самарская область",          "slug": "samara"},
    {"city": "Омск",               "region": "Омская область",             "slug": "omsk"},
    {"city": "Ростов-на-Дону",     "region": "Ростовская область",         "slug": "rostov-na-donu"},
    {"city": "Уфа",                "region": "Башкортостан",               "slug": "ufa"},
    {"city": "Красноярск",         "region": "Красноярский край",          "slug": "krasnoyarsk"},
    {"city": "Воронеж",            "region": "Воронежская область",        "slug": "voronezh"},
    {"city": "Пермь",              "region": "Пермский край",              "slug": "perm"},
    {"city": "Волгоград",          "region": "Волгоградская область",      "slug": "volgograd"},
    {"city": "Краснодар",          "region": "Краснодарский край",         "slug": "krasnodar"},
    {"city": "Тюмень",             "region": "Тюменская область",          "slug": "tyumen"},
    {"city": "Саратов",            "region": "Саратовская область",        "slug": "saratov"},
    {"city": "Тольятти",           "region": "Самарская область",          "slug": "tolyatti"},
    {"city": "Ижевск",             "region": "Удмуртия",                   "slug": "izhevsk"},
    {"city": "Барнаул",            "region": "Алтайский край",             "slug": "barnaul"},
    {"city": "Ульяновск",          "region": "Ульяновская область",        "slug": "ulyanovsk"},
    {"city": "Иркутск",            "region": "Иркутская область",          "slug": "irkutsk"},
    {"city": "Хабаровск",          "region": "Хабаровский край",           "slug": "habarovsk"},
    {"city": "Махачкала",          "region": "Дагестан",                   "slug": "mahachkala"},
    {"city": "Владивосток",        "region": "Приморский край",            "slug": "vladivostok"},
    {"city": "Ярославль",          "region": "Ярославская область",        "slug": "yaroslavl"},
    {"city": "Оренбург",           "region": "Оренбургская область",       "slug": "orenburg"},
    {"city": "Томск",              "region": "Томская область",            "slug": "tomsk"},
    {"city": "Кемерово",           "region": "Кемеровская область",        "slug": "kemerovo"},
    {"city": "Новокузнецк",        "region": "Кемеровская область",        "slug": "novokuznetsk"},
    {"city": "Рязань",             "region": "Рязанская область",          "slug": "ryazan"},
    {"city": "Набережные Челны",   "region": "Татарстан",                  "slug": "naberezhnie_chelny"},
    {"city": "Астрахань",          "region": "Астраханская область",       "slug": "astrahan"},
    {"city": "Киров",              "region": "Кировская область",          "slug": "kirov"},
    {"city": "Пенза",              "region": "Пензенская область",         "slug": "penza"},
    {"city": "Севастополь",        "region": "Севастополь",                "slug": "sevastopol"},
    {"city": "Липецк",             "region": "Липецкая область",           "slug": "lipetsk"},
    {"city": "Балашиха",           "region": "Московская область",         "slug": "balashiha"},
    {"city": "Чебоксары",          "region": "Чувашия",                    "slug": "cheboksary"},
    {"city": "Калининград",        "region": "Калининградская область",    "slug": "kaliningrad"},
    {"city": "Тула",               "region": "Тульская область",           "slug": "tula"},
    {"city": "Ставрополь",         "region": "Ставропольский край",        "slug": "stavropol"},
    {"city": "Курск",              "region": "Курская область",            "slug": "kursk"},
    {"city": "Улан-Удэ",           "region": "Бурятия",                    "slug": "ulan-ude"},
    {"city": "Сочи",               "region": "Краснодарский край",         "slug": "sochi"},
    {"city": "Тверь",              "region": "Тверская область",           "slug": "tver"},
    {"city": "Магнитогорск",       "region": "Челябинская область",        "slug": "magnitogorsk"},
    {"city": "Иваново",            "region": "Ивановская область",         "slug": "ivanovo"},
    {"city": "Брянск",             "region": "Брянская область",           "slug": "bryansk"},
    {"city": "Белгород",           "region": "Белгородская область",       "slug": "belgorod"},
    {"city": "Сургут",             "region": "Ханты-Мансийский АО",        "slug": "surgut"},
    {"city": "Владимир",           "region": "Владимирская область",       "slug": "vladimir"},
    {"city": "Чита",               "region": "Забайкальский край",         "slug": "chita"},
    {"city": "Архангельск",        "region": "Архангельская область",      "slug": "arhangelsk"},
    {"city": "Нижний Тагил",       "region": "Свердловская область",       "slug": "nižniy_tagil"},
    {"city": "Смоленск",           "region": "Смоленская область",         "slug": "smolensk"},
    {"city": "Калуга",             "region": "Калужская область",          "slug": "kaluga"},
    {"city": "Саранск",            "region": "Мордовия",                   "slug": "saransk"},
    {"city": "Череповец",          "region": "Вологодская область",        "slug": "cherepovec"},
    {"city": "Курган",             "region": "Курганская область",         "slug": "kurgan"},
    {"city": "Орёл",               "region": "Орловская область",          "slug": "orel"},
    {"city": "Вологда",            "region": "Вологодская область",        "slug": "vologda"},
    {"city": "Подольск",           "region": "Московская область",         "slug": "podolsk"},
    {"city": "Грозный",            "region": "Чечня",                      "slug": "groznyy"},
    {"city": "Мурманск",           "region": "Мурманская область",         "slug": "murmansk"},
    {"city": "Тамбов",             "region": "Тамбовская область",         "slug": "tambov"},
    {"city": "Петрозаводск",       "region": "Карелия",                    "slug": "petrozavodsk"},
    {"city": "Стерлитамак",        "region": "Башкортостан",               "slug": "sterlitamak"},
    {"city": "Нижневартовск",      "region": "Ханты-Мансийский АО",        "slug": "nizhnevartovsk"},
    {"city": "Кострома",           "region": "Костромская область",        "slug": "kostroma"},
    {"city": "Новороссийск",       "region": "Краснодарский край",         "slug": "novorossiysk"},
    {"city": "Йошкар-Ола",         "region": "Марий Эл",                   "slug": "yoshkar-ola"},
    {"city": "Химки",              "region": "Московская область",         "slug": "himki"},
    {"city": "Таганрог",           "region": "Ростовская область",         "slug": "taganrog"},
]

# Категория по умолчанию для кровли на Авито
AVITO_CATEGORY = "predlozheniya_uslug/stroitelstvo/krovlya"

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

def make_avito_url(slug, category=AVITO_CATEGORY):
    """Генерирует URL для поиска объявлений по городу на Авито."""
    return f"https://www.avito.ru/{slug}/{category}"

def load_cities_from_json(filepath="cities_list.json"):
    """Загружает список городов из JSON-файла.
    Если файл не найден — возвращает встроенный список cities_100kplus.
    Автоматически генерирует URL Авито для каждого города."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        result = []
        for item in data:
            city_name = item.get("city") or item.get("name", "")
            region = item.get("region", "")
            slug = item.get("slug", "")
            url = item.get("url", "")
            # Если URL пустой, но есть slug — генерируем
            if not url and slug:
                url = make_avito_url(slug)
            result.append({"city": city_name, "name": city_name, "region": region, "slug": slug, "url": url})
        return result
    except FileNotFoundError:
        print(f"[avito_cities] Файл {filepath} не найден, используем встроенный список.")
        result = []
        for c in cities_100kplus:
            url = make_avito_url(c["slug"]) if c.get("slug") else ""
            result.append({"city": c["city"], "name": c["city"], "region": c["region"], "slug": c.get("slug",""), "url": url})
        return result

if __name__ == "__main__":
    with open("cities_list.json", "w", encoding="utf-8") as f:
        json.dump(cities_100kplus, f, ensure_ascii=False, indent=2)
    print(f"Список из {len(cities_100kplus)} городов сохранен в cities_list.json")
