from utils import Dicts
from vacancies_parser import DataSet
from table_printer import TablePrinter
from stats_processor import Stats, Report


def print_vacancies_table(data):
    """
    Выводит таблицу с вакансиями в консоль

    Args:
        data (DataSet): DataSet вакансий
    """
    printer = TablePrinter(data)
    printer.print_table(Dicts.dic_naming)


def report_stats(data):
    """
    Создаёт статистический отчёт о вакансиях

    Args:
        data (DataSet): DataSet вакансий
    """
    stats = Stats(data)
    stats.print_full_stats()
    report = Report(stats.profession,
                    stats.year_salary_dynamics,
                    stats.num_of_vacancies_per_year,
                    stats.year_salary_dynamics_for_prof,
                    stats.num_of_vacancies_per_year_for_prof,
                    stats.salary_levels_of_areas,
                    stats.vacancy_fractions_of_areas)

    Report.generate_excel(
        profession=report.profession,
        year_salary_dynamics=report.year_salary_dynamics,
        num_of_vacancies_per_year=report.num_of_vacancies_per_year,
        year_salary_dynamics_for_prof=report.year_salary_dynamics_for_prof,
        num_of_vacancies_per_year_for_prof=report.num_of_vacancies_per_year_for_prof,
        salary_levels_of_areas=report.salary_levels_of_areas,
        vacancy_fractions_of_areas=report.vacancy_fractions_of_areas
    )

    Report.generate_image(
        profession=report.profession,
        year_salary_dynamics=report.year_salary_dynamics,
        num_of_vacancies_per_year=report.num_of_vacancies_per_year,
        year_salary_dynamics_for_prof=report.year_salary_dynamics_for_prof,
        num_of_vacancies_per_year_for_prof=report.num_of_vacancies_per_year_for_prof,
        salary_levels_of_areas=report.salary_levels_of_areas,
        vacancy_fractions_of_areas=report.vacancy_fractions_of_areas
    )

    Report.generate_pdf(
        profession=report.profession,
        year_salary_dynamics=report.year_salary_dynamics,
        num_of_vacancies_per_year=report.num_of_vacancies_per_year,
        year_salary_dynamics_for_prof=report.year_salary_dynamics_for_prof,
        num_of_vacancies_per_year_for_prof=report.num_of_vacancies_per_year_for_prof,
        salary_levels_of_areas=report.salary_levels_of_areas,
        vacancy_fractions_of_areas=report.vacancy_fractions_of_areas,
        graph_path=r"C:\Okladnikov\graph.png"
    )


commands = {'Вакансии': lambda data: print_vacancies_table(data),
            'Статистика': lambda data: report_stats(data)}

command = input('Введите команду: ')
if command not in list(commands.keys()):
    print('Неизвестная команда!')
else:
    commands[command](DataSet(input('Введите данные для печати: ')))
