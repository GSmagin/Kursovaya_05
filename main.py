from confing import API_HH_RU_VACANCIES
from src.utils import get_hh_data, save_to_file_json


def main():
    company_ids = ['3127']

    save_to_file_json(get_hh_data(API_HH_RU_VACANCIES, company_ids), "vacations.json")
    # print(get_hh_data(API_HH_RU_VACANCIES, company_ids))


if __name__ == "__main__":
    main()
