from src.class_dbmanager import DBManager
from confing import API_HH_RU_EMPLOYERS, API_HH_RU_VACANCIES, config_connectdb
from src.utils import (search_companies, get_hh_data, create_tables, insert_data,
                       clear_database, save_to_file_json)


class Menu:

    def __init__(self):
        self.companies = []
        self.company_list = []
        self.config = config_connectdb()

    def show_main_menu(self):
        """Главное меню"""
        print("Главное меню:")
        print("1. Выбор списка компаний поиска вакансий")
        print("2. Подменю запроса и поиска")
        print("3. Очистить базу данных")
        print("4. Выход")

    def show_company_selection_menu(self):
        """Меню выбора списка компаний"""
        print("1. Готовый список")
        print("2. Создать свой список")
        print("3. Запустить поиск вакансий и запись в базу данных")
        print("4. Выход в главное меню")

    def show_search_submenu(self):
        """Подменю запроса и поиска"""
        print("Подменю запроса и поиска:")
        print("1. Выводит список всех компаний и количество вакансий у каждой компании")
        print("2. Выводит список всех вакансий с указанием названия компании,\n"
              " названия вакансии и зарплаты и ссылки на вакансию")
        print("3. Выводит среднюю зарплату по вакансиям")
        print("4. Выводит список всех вакансий, у которых зарплата выше средней по всем вакансиям")
        print("5. Поиск вакансий по ключевому слову")
        print("6. Выход в главное меню")

    def select_company_list(self):
        """Выбор списка компаний"""
        # self.company_list = ['3127']
        self.company_list = ['3127',
                             '2748',
                             '1740',
                             '1473866',
                             '4023',
                             '6167349',
                             '3776',
                             '15478',
                             '916364',
                             '740'
                             ]
        print("Выбран список компаний:\n"
              "1. 'МегаФон', 'https://hh.ru/employer/3127'\n"
              "2. 'Ростелеком', 'https://hh.ru/employer/2748'\n"
              "3. 'Яндекс', 'https://hh.ru/employer/1740'\n"
              "4. 'Сбербанк-Сервис', 'https://hh.ru/employer/1473866'\n"
              "5. 'Райффайзен Банк', 'https://hh.ru/employer/4023'\n"
              "6. 'Garant Bank', 'https://hh.ru/employer/6167349'\n"
              "7. 'МТС', 'https://hh.ru/employer/3776'\n"
              "8. 'VK', 'https://hh.ru/employer/15478'\n"
              "9. '585, Золотой', 'https://hh.ru/employer/916364'\n"
              "10. 'Норникель', 'https://hh.ru/employer/740'\n")

    def select_company_list_search(self):
        """Создание списка компаний для поиска"""
        self.company_list = []
        self.company_list = search_companies(API_HH_RU_EMPLOYERS)
        print("Создан список компаний: ")

    def search_vacancies(self):
        """Поиск вакансий"""
        print("Запуск поиска вакансий...")
        vacancy = get_hh_data(API_HH_RU_VACANCIES, self.company_list)
        save_to_file_json(vacancy, 'vacancy.json')
        create_tables("vacancy_db", self.config)
        insert_data(vacancy, "vacancy_db", self.config)

    def clear_database(self):
        """Очистка базы данных"""
        print("Очистка базы данных...")
        clear_database("vacancy_db", self.config)
        print("База данных очищена")

    def run(self):
        """Запуск программы"""
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
                        dbmanager = DBManager("vacancy_db", self.config)
                        dbmanager.get_companies_and_vacancies_count()
                    elif search_choice == '2':
                        print(
                            "Вы выбрали: Выводит список всех вакансий с указанием названия компании,\n"
                            " названия вакансии и зарплаты и ссылки на вакансию")
                        dbmanager = DBManager("vacancy_db", self.config)
                        dbmanager.get_all_vacancies()
                    elif search_choice == '3':
                        print("Вы выбрали: Выводит среднюю зарплату по вакансиям")
                        dbmanager = DBManager("vacancy_db", self.config)
                        dbmanager.get_avg_salary()
                    elif search_choice == '4':
                        print("Вы выбрали: Выводит список всех вакансий, у которых зарплата\n"
                              " выше средней по всем вакансиям")
                        dbmanager = DBManager("vacancy_db", self.config)
                        dbmanager.get_vacancies_with_higher_salary()
                    elif search_choice == '5':
                        print("Вы выбрали: Поиск вакансий по ключевому")
                        keyword = input("Введите ключевое слово поиска: ")
                        dbmanager = DBManager("vacancy_db", self.config)
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
