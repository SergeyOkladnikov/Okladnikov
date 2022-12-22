from vacancies_parser import DataSet, Salary
from unittest import TestCase, main


class GetFilteredVacanciesTests(TestCase):
    def setUp(self):
        self.data = DataSet('filtration_test.csv')

    def test_name_filter(self):
        self.assertEqual([x.name for x in self.data.get_filtered_vacancies('Название: HTML-верстальщик')], ['HTML-верстальщик'])

    def test_description_filter(self):
        self.assertEqual([x.name for x in self.data.get_filtered_vacancies('Описание: XXXX')], ['HTML-верстальщик', 'Information Security Policy Specialist (Methodology)'])

    def test_key_skills_filter(self):
        self.assertEqual([x.name for x in self.data.get_filtered_vacancies('Навыки: HTML5, CSS3')], ['HTML-верстальщик', 'HTML-верстальщик (remote)'])

    def test_experience_id_filter(self):
        self.assertEqual([x.name for x in self.data.get_filtered_vacancies('Опыт работы: Более 6 лет')], ['Senior Python Developer (Crypto)', 'Information Security Policy Specialist (Methodology)', 'Reporting and Visualization Analyst (BI)'])

    def test_premium_filter(self):
        self.assertEqual([x.name for x in self.data.get_filtered_vacancies('Премиум-вакансия: Да')], ['Node.js backend разработчик'])

    def test_employer_name_filter(self):
        self.assertEqual([x.name for x in self.data.get_filtered_vacancies('Компания: ПМЦ Авангард')], ['Руководитель проекта по системам связи и информационным технологиям'])

    def test_salary_filter(self):
        self.assertEqual([x.name for x in self.data.get_filtered_vacancies('Оклад: 130000')], ['HTML-верстальщик (remote)',
                                                                                               'Руководитель - администратор магазина компьютерной техники',
                                                                                               'Инженер AV (мультимедиа) оборудование',
                                                                                               'Web-разработчик PHP (full stack)'])

    def test_salary_gross_filter(self):
        self.assertEqual([x.name for x in self.data.get_filtered_vacancies('Оклад указан до вычета налогов: Да')], ['Монтажник связи (линейщик)', 'Инженер AV (мультимедиа) оборудование'])

    def test_salary_currency_filter(self):
        self.assertEqual([x.name for x in self.data.get_filtered_vacancies('Идентификатор валюты оклада: BYR')], ['HTML-верстальщик', 'Инженер технической поддержки/HelpDesk'])

    def test_area_name_filter(self):
        self.assertEqual([x.name for x in self.data.get_filtered_vacancies('Название региона: Санкт-Петербург')], ['Руководитель проекта по системам связи и информационным технологиям',
                                                                                                                   'Node.js backend разработчик',
                                                                                                                   'Инженер технической поддержки'])

    def test_published_at_filter(self):
        self.assertEqual([x.name for x in self.data.get_filtered_vacancies('Дата публикации вакансии: 17.07.2022')], ['Руководитель проекта по системам связи и информационным технологиям',
                                                                                                                      'Инженер технической поддержки/HelpDesk',
                                                                                                                      'Монтажник связи (линейщик)',
                                                                                                                      'Инженер технической поддержки'])

    def test_filter_with_empty_criterion(self):
        self.assertEqual(len(self.data.get_filtered_vacancies('')), len(self.data.vacancies_objects))


class SalaryTests(TestCase):
    def test_salary_type(self):
        self.assertEqual(type(Salary('10000', '20000', 'True', 'RUR')).__name__, 'Salary')

    def test_salary_from(self):
        self.assertEqual(Salary('10000.0', '20000', 'True', 'RUR').salary_from, '10000.0')

    def test_salary_to(self):
        self.assertEqual(Salary('10000.0', '20000.1', 'True', 'RUR').salary_to, '20000.1')

    def test_salary_gross(self):
        self.assertEqual(Salary('10000.0', '20000.1', 'True', 'RUR').salary_gross, 'True')

    def test_salary_currency(self):
        self.assertEqual(Salary('10000.0', '20000.1', 'True', 'RUR').salary_currency, 'RUR')


class GetSalaryInRurTests(TestCase):
    def test_salary_from(self):
        self.assertEqual(Salary('200', '300', 'True', 'EUR').get_salary_in_rur().salary_from, '11980.0')

    def test_salary_to(self):
        self.assertEqual(Salary('200', '300', 'True', 'EUR').get_salary_in_rur().salary_to, '17970.0')

    def test_salary_gross(self):
        self.assertEqual(Salary('200', '300', 'True', 'EUR').get_salary_in_rur().salary_gross, 'True')

    def test_salary_currency(self):
        self.assertEqual(Salary('200', '300', 'True', 'EUR').get_salary_in_rur().salary_currency, 'RUR')


class DataSetTests(TestCase):
    def test_dataset_type(self):
        self.assertEqual(type(DataSet('v.csv')).__name__, 'DataSet')

    def test_file_name(self):
        self.assertEqual(DataSet('v.csv').file_name, 'v.csv')

    def test_vacancies_objects_type(self):
        self.assertEqual(type(DataSet('v.csv').vacancies_objects).__name__, 'list')

    def test_vacancy_type(self):
        self.assertEqual(type(DataSet('v.csv').vacancies_objects[0]).__name__, 'Vacancy')

    def test_vacancy_key_skills_type(self):
        self.assertEqual(type(DataSet('v.csv').vacancies_objects[0].key_skills).__name__, 'list')

    def test_vacancy_key_skills(self):
        self.assertEqual(DataSet('v.csv').vacancies_objects[0].key_skills, ['Организаторские навыки',
                                                                            'Проведение презентаций',
                                                                            'MS PowerPoint',
                                                                            'Информационные технологии',
                                                                            'Аналитическое мышление',
                                                                            'Автоматизированное рабочее место (АРМ)',
                                                                            'техническая грамотность'])


class DataSetSortTests(TestCase):
    def test_lexicographic_sort(self):
        data = DataSet('sorting_test.csv')
        data.sort('Название', 'Нет')
        self.assertEqual([x.name for x in data.vacancies_objects],
                         ['HTML-верстальщик', 'HTML-верстальщик (remote)',
                          'Information Security Policy Specialist (Methodology)', 'Senior Python Developer (Crypto)',
                          'Руководитель проекта по системам связи и информационным технологиям']
                         )

    def test_list_length_sort(self):
        data = DataSet('sorting_test.csv')
        data.sort('Навыки', 'Нет')
        self.assertEqual([x.name for x in data.vacancies_objects],
                         ['Information Security Policy Specialist (Methodology)', 'Senior Python Developer (Crypto)',
                          'Руководитель проекта по системам связи и информационным технологиям',
                          'HTML-верстальщик (remote)', 'HTML-верстальщик']
                         )

    def test_experience_sort(self):
        data = DataSet('sorting_test.csv')
        data.sort('Опыт работы', 'Нет')
        self.assertEqual([x.name for x in data.vacancies_objects],
                         ['HTML-верстальщик', 'HTML-верстальщик (remote)',
                          'Руководитель проекта по системам связи и информационным технологиям',
                          'Senior Python Developer (Crypto)', 'Information Security Policy Specialist (Methodology)']
                         )

    def test_mean_salary_sort(self):
        data = DataSet('sorting_test.csv')
        data.sort('Оклад', 'Нет')
        self.assertEqual([x.name for x in data.vacancies_objects],
                         ['Руководитель проекта по системам связи и информационным технологиям', 'HTML-верстальщик',
                          'HTML-верстальщик (remote)', 'Senior Python Developer (Crypto)',
                          'Information Security Policy Specialist (Methodology)']
                         )

    def test_date_sort(self):
        data = DataSet('sorting_test.csv')
        data.sort('Дата публикации вакансии', 'Нет')
        self.assertEqual([x.name for x in data.vacancies_objects],
                         ['Senior Python Developer (Crypto)', 'HTML-верстальщик', 'HTML-верстальщик (remote)',
                          'Information Security Policy Specialist (Methodology)',
                          'Руководитель проекта по системам связи и информационным технологиям']
                         )

    def test_reverse_sort(self):
        data = DataSet('sorting_test.csv')
        data.sort('Название', 'Да')
        self.assertEqual([x.name for x in data.vacancies_objects],
                         ['Руководитель проекта по системам связи и информационным технологиям',
                          'Senior Python Developer (Crypto)', 'Information Security Policy Specialist (Methodology)',
                          'HTML-верстальщик (remote)', 'HTML-верстальщик']
                         )


if __name__ == '__main__':
    main()

