import psycopg2


class DBManager:

    def __init__(self, db_name: str, params: dict) -> None:
        self.conn = psycopg2.connect(dbname=db_name, **params)
        self.cur = self.conn.cursor()

    # def __del__(self):
    #     if self.conn is not None:
    #         self.conn.close()
    #         # print("Соединение закрыто.")

    def get_connection(self, request_text: str):
        """Получение соединения с базой данных"""
        self.cur = self.conn.cursor()
        with self.cur as cursor:
            cursor.execute(request_text)
            rows = cursor.fetchall()
        return rows

    def get_companies_and_vacancies_count(self) -> None:
        """Вывод списка компаний и количество вакансий """
        request_text = """SELECT 
        Companies.name, 
        COUNT(Vacancies.id_vacancy) AS vacancies_count
        FROM Companies LEFT JOIN Vacancies ON Companies.id_company = Vacancies.id_company
        GROUP BY Companies.id_company, Companies.name;"""

        response_database = self.get_connection(request_text)

        print("\nСписок компаний и количество вакансий\n")
        for rdb in response_database:
            print(f"Название компании - {rdb[0]};\n"
                  f"Количество открытых вакансий - {rdb[1]}.\n")

    def get_all_vacancies(self) -> None:
        """Вывод всех вакансий"""
        request_text = """SELECT 
        Companies.name AS Company_name,
        vacancies.name as name_vacancies,
        salary_from, 
        salary_to, 
        Vacancies.currency, 
        Vacancies.alternate_url AS vacancy_url
        FROM public.vacancies
        LEFT JOIN Companies ON vacancies.id_company = Companies.id_company"""

        response_database = self.get_connection(request_text)

        print("\nСписок всех вакансий:\n")
        for rdb in response_database:
            print(f"Название компании  - {rdb[0]};\n"
                  f"Название вакансии - {rdb[1]};\n"
                  f"Зарплата от - {'Зарплата не указана' if rdb[2] is None else rdb[2]};\n"
                  f"Зарплата до - {'Зарплата не указана' if rdb[3] is None else rdb[3]};\n"
                  f"Валюта - {'Валюта не указана' if rdb[4] is None else rdb[4]};\n"
                  f"Ссылка на вакансию - {rdb[5]}.\n")

    def get_avg_salary(self) -> None:
        """Вывод средней зарплаты"""
        request_text = """SELECT AVG(salary_from) AS avg_salary FROM Vacancies;"""
        request_text = """SELECT ROUND(AVG(salary_from + salary_to) / 2) AS avg_salary
        FROM Vacancies;"""

        response_database = self.get_connection(request_text)

        for rdb in response_database:
            print(f"\nСредняя зарплата по вакансиям - {rdb[0]}.")

    def get_vacancies_with_higher_salary(self) -> None:
        """Вывод списка вакансий с наибольшей зарплатой"""
        request_text = """SELECT 
        Vacancies.name AS vacancy_name,
        Vacancies.salary_from,
        Vacancies.salary_to,
        Vacancies.currency,
        Companies.name AS company_name
        FROM Vacancies
        INNER JOIN Companies ON Vacancies.id_company = Companies.id_company
        WHERE (Vacancies.salary_from + Vacancies.salary_to) / 2 > (
        SELECT AVG(salary_from + salary_to) / 2 
        FROM Vacancies);"""

        response_database = self.get_connection(request_text)

        print("\nВакансии с зарплатой выше среднего\n")
        for rdb in response_database:
            print(f"Название вакансии  - {rdb[0]};\n"
                  f"Зарплата - {rdb[1]}.\n")

    def get_vacancies_with_keyword(self, keyword: str) -> None:
        """Вывод списка вакансий с указанным названием"""
        request_text = (f"""SELECT
        Vacancies.name AS vacancy_name, 
        Companies.name AS company_name,
        salary_from, 
        salary_to, 
        Vacancies.currency,
        Vacancies.alternate_url
        FROM Vacancies 
        INNER JOIN Companies ON Vacancies.id_company = Companies.id_company 
        WHERE LOWER(Vacancies.name) LIKE '%' || LOWER('{keyword}') || '%';""")

        response_database = self.get_connection(request_text)

        print("\nСписок найденных вакансий\n")
        for rdb in response_database:
            print(f"Название вакансии  - {rdb[0]};\n"
                  f"Название компании - {rdb[1]};\n"
                  f"Зарплата от - {'Зарплата не указана' if rdb[2] is None else rdb[2]};\n"
                  f"Зарплата до - {'Зарплата не указана' if rdb[3] is None else rdb[3]};\n"
                  f"Валюта - {'Валюта не указана' if rdb[4] is None else rdb[4]};\n"
                  f"Ссылка на вакансию - {rdb[5]}.\n")

    # def __del__(self):
    #     if self.conn is not None:
    #         self.conn.close()
    #         # print("Соединение закрыто.")