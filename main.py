import requests

from confing import API_HH_RU_VACANCIES, API_HH_RU_EMPLOYERS, config
from src.utils import (get_hh_company, save_to_file_json, get_count_pages,
                       get_hh_data, create_database, save_data_to_database,
                       close_connect_database, create_tables, insert_data)


def main():
    vacancies_list = [
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

    # company_id_list = get_hh_company(API_HH_RU_EMPLOYERS, 'мегафон')
    # print(company_id_list)
    # save_to_file_json(company_id_list, "company_id_list.json")


    vacancy = get_hh_data(API_HH_RU_VACANCIES, vacancies_list)
    # #print(vacancy)
    save_to_file_json(vacancy, "vacancy.json")

   #close_connect_database("vacancydb", config())

    create_tables("vacancydb", config())
    insert_data(vacancy, "vacancydb", config())

    #create_database("vacancydb", config())
    #save_data_to_database(vacancy, "vacancydb", config())


if __name__ == "__main__":
    main()
