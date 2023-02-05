import os
import shutil
import pandas as pd
from os.path import getctime
import datetime


def folder_cleaner(folder):
    """
    Сleaning the contents of a folder
    
    :param folder: path to folder
    :return:
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def create_folder_for_answer():
    """
    Сreate folder for answers
    
    :param 
    :return: folder_name
    """
    folder_name = os.path.basename(__file__).split('.')[0]
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    else:
        folder_cleaner(folder_name)

    return folder_name


def main():
    # create or clean folder for answers
    folder_name = create_folder_for_answer()

    upload_frame = pd.read_excel('Задание 1.xlsx', sheet_name=0)

    # Formatting second list
    print(upload_frame.to_string)

    customer_costs_df = upload_frame.groupby(['Заказчик', "Задача"]).agg({'Залогированные часы': 'sum'})

    # Added results for each customer
    each_customer_sum_df = customer_costs_df.groupby(level=0).sum()
    new_cols = list(
        zip(each_customer_sum_df.index.get_level_values(0), [' Итог по заказчику:'] * len(each_customer_sum_df.index)))
    each_customer_sum_df.index = pd.MultiIndex.from_tuples(new_cols)

    customer_costs_df = pd.concat([customer_costs_df, each_customer_sum_df]).sort_index().sort_values(
        ['Заказчик', "Задача", 'Залогированные часы'], ascending=False, axis=0)

    # Added overall result
    customer_costs_df = customer_costs_df.reindex([*customer_costs_df.index, (" ", "Общий Итог")])
    customer_costs_df.loc[[(' ', 'Общий Итог')], 'Залогированные часы'] = sum(
        each_customer_sum_df['Залогированные часы'])
    print(customer_costs_df)

    # Formatting third list
    # Create df with expended hours
    employee_hours_df = upload_frame.groupby(['Исполнитель'], as_index=False).agg({'Залогированные часы': 'sum'})
    employee_hours_df.columns = ['Имя', 'Часы']

    # Upload salaries list 
    salary_df = pd.read_excel('Задание 1.xlsx', sheet_name=2)

    # Filling nan to correct digits
    salary_df[['Имя', 'Часы']] = employee_hours_df
    salary_df['Стоимость часа'] = round((salary_df['Выплата за месяц (рублей)'] / salary_df['Часы']), 2)
    print(salary_df)

    # Write to excel
    file_name = os.path.join(folder_name, folder_name + '_answer.xlsx')
    writer = pd.ExcelWriter(file_name)
    upload_frame.to_excel(writer, sheet_name="Проекты (выгрузка)", index=False)
    customer_costs_df.to_excel(writer, sheet_name="Затраты заказчика", header=False)
    salary_df.to_excel(writer, sheet_name="Зарплаты", index=False)
    # writer.save()
    writer.close()


if __name__ == '__main__':
    try:
        # ALL RPA TECHNOLOGY MUST RUN SMOOTHLY
        global upload_file_path
        upload_file_path = 'Задание 1.xlsx'

        # Сhecking a new upload file for create report
        current_month = datetime.date.today().strftime("%m.%Y")
        file_month = datetime.datetime.fromtimestamp(getctime(upload_file_path)).strftime('%m.%Y')

        if current_month == file_month and os.path.exists(upload_file_path):
            main()
        else:
            print(f"Need to update upload file!")

    except Exception as e:
        print(f"Something go wrong")
        print(e)
