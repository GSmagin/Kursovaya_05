import json
import requests
import psycopg2


def get_hh_company(api_url, company_name):
    # в разработке поиск компаний в hh.ru
    """Поиск компаний в hh.ru
    :param api_url: (str) публичный ключ к API
    :param company_name: (str) название компании
    :return:"""
    company_list = requests.get(api_url, params={
        "text": company_name,
        "only_with_vacancies": 'true'
    })
    company_list = company_list.json().get("items")

    return company_list


def get_count_pages(api_url: str, company_id: str) -> int:
    """
    Получает количество страниц в файле JSON
    :param api_url: (str) публичный ключ к API
    :param company_id: (str) название компании
    :return: (int) количество страниц
    """
    try:
        hh_data = requests.get(api_url, params={
            "employer_id": company_id,
            "per_page": 100,
            "area": 1
        })

        hh_data.raise_for_status()

        # Проверяем, корректный ли JSON-ответ
        json_data = hh_data.json()
        if "pages" in json_data:
            return json_data["pages"]
        else:
            raise ValueError("Ответ JSON не содержит ключ 'pages'")

    except requests.exceptions.RequestException as e:
        # Ошибки подключения
        print(f"Ошибка при подключении к API: {e}")
        # return -1

    except (KeyError, ValueError) as e:
        # Ошибки разбора JSON или отсутствие ключа
        print(f"Ошибка при разборе JSON: {e}")
        # return -1


def get_hh_data(api_url: str, companies_id: list[str]) -> list[dict]:
    """
    Получает данные о компаниях и вакансиях с помощью API HH.ru
    :param api_url: (str) публичный ключ к API
    :param companies_id: (list[str]) список компаний

    :return: (list[dict]) список данных о компаниях и их вакансиях
    """

    vacancy = []
    for company_id in companies_id:
        try:
            page = 0
            pages = get_count_pages(api_url, company_id)
            while page != pages:
                hh_data = requests.get(api_url, params={
                    "employer_id": company_id,
                    "page": page,
                    "per_page": 100,
                    "area": 1
                })

                hh_data.raise_for_status()

                vacancy.extend(hh_data.json().get('items'))
                print(f"Получено {len(vacancy)} вакансий")
                page += 1

        except requests.exceptions.RequestException as e:
            # Ошибки подключения
            print(f"Ошибка при подключении к API: {e}")
            continue

        except (KeyError, ValueError) as e:
            # Ошибки JSON или отсутствие ключа
            print(f"Ошибка при разборе JSON: {e}")
            continue

    return vacancy


def save_to_file_json(vacancies: list[dict], filename: str) -> None:
    """Запись списка вакансий в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        vacancies_json = json.dumps(vacancies, ensure_ascii=False, indent=4)
        f.write(vacancies_json)


def close_connect_database(db_name: str, params: dict) -> None:
    """Закрытие соединения с базой данных
    :param db_name: (str) название базы данных
    :param params: (dict) параметры подключения к базе данных
    """
    conn = psycopg2.connect(dbname=db_name, **params)
    conn.close()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE "
                   f"datname = '{db_name}' AND leader_pid IS NULL")
    conn.close()


def clear_database(db_name: str, params: dict) -> None:
    """
    Очищает базу данных о компаниях и их вакансиях.
    :param db_name: (str) название базы данных
    :param params: (dict) параметры подключения к базе данных
    """
    close_connect_database(db_name, params)

    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cursor.execute(f"CREATE DATABASE {db_name}")

    conn.close()


# Функция для создания таблиц в базе данных
def create_tables(db_name: str, params: dict) -> None:
    clear_database(db_name, params)  # Очищает базу данных о компаниях и их вакансиях

    conn = psycopg2.connect(dbname=db_name, **params)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Companies (
                        id_company TEXT PRIMARY KEY,
                        name TEXT,
                        url TEXT,
                        alternate_url TEXT,
                        logo_url_original TEXT,
                        logo_url_240 TEXT,
                        vacancies_url TEXT,
                        accredited_it_employer BOOLEAN,
                        trusted BOOLEAN
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Vacancies (
                        id_vacancy TEXT PRIMARY KEY,
                        id_company TEXT,
                        name TEXT,
                        city TEXT,
                        street TEXT,
                        building TEXT,
                        published_at TIMESTAMP,
                        created_at TIMESTAMP,
                        apply_alternate_url TEXT,
                        alternate_url TEXT,
                        requirement TEXT,
                        responsibility TEXT,
                        schedule_name TEXT,
                        experience_name TEXT,
                        employment_name TEXT,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        currency VARCHAR(10),
                        FOREIGN KEY (id_company) REFERENCES Companies(id_company)
                    )''')

    conn.commit()
    conn.close()


# Функция для добавления данных в таблицы
def insert_data(data: list[dict], db_name: str, params: dict) -> None:
    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cursor:
        # Вставка данных в таблицу Companies
        for item in data:
            id_company = item['employer']['id']
            name = item['employer']['name']
            url = item['employer']['url']
            alternate_url = item['employer']['alternate_url']
            logo_url_original = item['employer']['logo_urls']['original']
            logo_url_240 = item['employer']['logo_urls']['240']
            vacancies_url = item['employer']['vacancies_url']
            accredited_it_employer = item['employer']['accredited_it_employer']

            cursor.execute(
                'INSERT INTO Companies\n'
                '                (id_company, \n'
                '                name, \n'
                '                url, \n'
                '                alternate_url, \n'
                '                logo_url_original, \n'
                '                logo_url_240, \n'
                '                vacancies_url, \n'
                '                accredited_it_employer)\n'
                '               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)\n'
                '                ON CONFLICT (id_company) DO NOTHING',
                (id_company,
                 name,
                 url,
                 alternate_url,
                 logo_url_original,
                 logo_url_240,
                 vacancies_url,
                 accredited_it_employer)
            )
            # Вставка данных в таблицу Vacancies
            address = item.get('address')
            if address:
                city = address.get('city')
                street = address.get('street')
                building = address.get('building')
            else:
                city = street = building = None

            id_vacancy = item['id']
            name = item['name']
            published_at = item['published_at']
            created_at = item['created_at']
            apply_alternate_url = item['apply_alternate_url']
            alternate_url = item['alternate_url']
            requirement = item.get('snippet').get('requirement', None)
            responsibility = item.get('snippet').get('responsibility', None)
            schedule_name = item.get('schedule').get('name', None)
            experience_name = item.get('experience').get('name', None)
            employment_name = item.get('employment').get('name', None)

            salary_info = item.get('salary')
            if salary_info:
                salary_from = salary_info.get('from')
                salary_to = salary_info.get('to')
                currency = salary_info.get('currency')
            else:
                salary_from = salary_to = currency = None

            cursor.execute(
                'INSERT INTO Vacancies\n'
                ' (id_vacancy, \n'
                'id_company, \n'
                'name, \n'
                'city, \n'
                'street, \n'
                'building, \n'
                'published_at, \n'
                'created_at, \n'
                'apply_alternate_url, \n'
                'alternate_url, \n'
                'requirement, \n'
                'responsibility, \n'
                'schedule_name, \n'
                'experience_name, \n'
                'employment_name, \n'
                'salary_from, \n'
                'salary_to, \n'
                'currency) \n'
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (id_vacancy,
                 id_company,
                 name,
                 city,
                 street,
                 building,
                 published_at,
                 created_at,
                 apply_alternate_url,
                 alternate_url,
                 requirement,
                 responsibility,
                 schedule_name,
                 experience_name,
                 employment_name,
                 salary_from,
                 salary_to,
                 currency)
            )
    conn.commit()
    conn.close()
    print('Запись в базу данных завершена')


def search_companies(api):
    selected_companies = []

    while True:
        keyword = input("Введите название компании (для выхода введите '00'): ")
        if keyword.lower() == '00':
            break

        companies = get_hh_company(api, keyword)
        if not companies:
            print("По вашему запросу ничего не найдено.")
            continue

        companies_sorted = [{"id": company.get("id"),
                             "name": company.get("name"),
                             "alternate_url": company.get("alternate_url")} for company in companies]

        print("Найденные компании:")
        for i, company in enumerate(companies_sorted):
            print(f"{i + 1}. {company['name']}")

        while True:
            choice = input("Выберите номера компаний для добавления в список (разделите номера пробелом): ")
            try:
                choices = [int(x) for x in choice.split()]
                for index in choices:
                    if 1 <= index <= len(companies_sorted):
                        selected_companies.append(companies_sorted[index - 1])
                    else:
                        print("Неверный номер компании. Пожалуйста, выберите снова.")
                break
            except ValueError:
                print("Пожалуйста, введите допустимые номера.")

        print("Выбранные компании:")
        for i, company in enumerate(selected_companies):
            print(f"{i + 1}. {company['name'], company['alternate_url']}")

        option = input("Хотите ли запустить новый поиск? (да/нет):")
        if option.lower() != 'да':
            break
    selected_companies_sorted = []
    for company in selected_companies:
        selected_companies_sorted.append(company.get("id"))
    print(selected_companies_sorted)
    return selected_companies_sorted
