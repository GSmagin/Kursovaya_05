from src.confing import *
from src.utils import *
from src.class_dbmanager import *


class Menu:

    def __init__(self):
        self.companies = {}
        self.vacancies = []
        self.company_list = []
        self.config = config()

    def show_main_menu(self):
        print("Главное меню:")
        print("1. Выбор списка компаний поиска вакансий")
        print("2. Подменю запроса и поиска")
        print("3. Очистить базу данных")
        print("4. Выход")

    def show_company_selection_menu(self):
        print("1. Готовый список")
        print("2. Создать свой список")
        print("3. Запустить поиск вакансий и запись в базу данных")
        print("4. Выход в главное меню")

    def show_search_submenu(self):
        print("Подменю запроса и поиска:")
        print("1. Выводит список всех компаний и количество вакансий у каждой компании")
        print("2. Выводит список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
        print("3. Выводит среднюю зарплату по вакансиям")
        print("4. Выводит список всех вакансий, у которых зарплата выше средней по всем вакансиям")
        print("5. Поиск вакансий по ключевому")
        print("6. Выход в главное меню")

    def select_company_list(self):
        self.company_list = [
            '1473866',
            '4023',
            '205',
            '4219',
            '23040',
            '740',
            '3838',
            '1057',
            '1180',
            '208707',
            '1740'
        ]
        print("Выбран список компаний: ", self.company_list)
        # Реализуйте соответствующий функционал

    def select_company_list_search(self):
        print("Выбор списка компаний поиска вакансий...")
        # Реализуйте соответствующий функционал

    def search_vacancies(self):
        print("Запуск поиска вакансий...")
        vacancy = get_hh_data(API_HH_RU_VACANCIES, self.company_list)
        create_tables("vacancydb", self.config)
        insert_data(vacancy, "vacancydb", self.config)

    def clear_database(self):
        print("Очистка базы данных...")
        clear_database("vacancydb", self.config)
        print("База данных очищена")

    def run(self):
        while True:
            self.show_main_menu()
            choice = input("Выберите пункт: ")
            if choice == '1':
                while True:
                    self.show_company_selection_menu()
                    company_choice = input("Выберите пункт: ")
                    if company_choice == '1':
                        print("Вы выбрали: Готовый список")
                        self.select_company_list()
                    elif company_choice == '2':
                        print("Вы выбрали: Создать свой список")
                        self.select_company_list_search()
                        # Добавьте соответствующий код для этой опции
                    elif company_choice == '3':
                        self.search_vacancies()
                    elif company_choice == '4':
                        break
                    else:
                        print("Некорректный ввод. Попробуйте снова.")
            elif choice == '2':
                while True:
                    self.show_search_submenu()
                    search_choice = input("Выберите пункт: ")
                    if search_choice == '1':
                        print("Вы выбрали: Выводит список всех компаний и количество вакансий у каждой компании")
                        dbmanager = DBManager("vacancydb", self.config)
                        dbmanager.get_companies_and_vacancies_count()
                    elif search_choice == '2':
                        print(
                            "Вы выбрали: Выводит список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
                        dbmanager = DBManager("vacancydb", self.config)
                        dbmanager.get_all_vacancies()
                    elif search_choice == '3':
                        print("Вы выбрали: Выводит среднюю зарплату по вакансиям")
                        dbmanager = DBManager("vacancydb", self.config)
                        dbmanager.get_avg_salary()
                    elif search_choice == '4':
                        print(
                            "Вы выбрали: Выводит список всех вакансий, у которых зарплата выше средней по всем вакансиям")
                        dbmanager = DBManager("vacancydb", self.config)
                        dbmanager.get_vacancies_with_higher_salary()
                    elif search_choice == '5':
                        print("Вы выбрали: Поиск вакансий по ключевому")
                        keyword = input("Введите ключевое слово поиска: ")
                        dbmanager = DBManager("vacancydb", self.config)
                        dbmanager.get_vacancies_with_keyword(keyword)
                    elif search_choice == '6':
                        break
                    else:
                        print("Некорректный ввод пункта меню. Попробуйте снова.")
            elif choice == '3':
                self.clear_database()
            elif choice == '4':
                print("До свидания!")
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")


# Пример использования:
menu = Menu()
menu.run()