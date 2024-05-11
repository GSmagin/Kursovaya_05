import psycopg2


class DBManager:

    def __init__(self, db_name: str, params: dict) -> None:
        self.conn = psycopg2.connect(dbname=db_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> None:
        with self.cur as cursor:
            cursor.execute(
                """
                SELECT Companies.name, COUNT(Vacancies.id_vacancy) AS vacancies_count
                FROM Companies
                LEFT JOIN Vacancies ON Companies.id_company = Vacancies.id_company
                GROUP BY Companies.id_company, Companies.name;

                """)
            rows = cursor.fetchall()
            print("\nСписок компаний и количество вакансий\n")
            for row in rows:
                print(f"Название компании - {row[0]}; Количество открытых вакансий - {row[1]}")

        self.conn.close()

    def get_all_vacancies():
        pass

    def get_avg_salary():
        pass

    def get_vacancies_with_higher_salary():
        pass

    def get_vacancies_with_keyword():
        pass
