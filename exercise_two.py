import os
import json
import shutil
import re


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


def write_answers(data, folder_name):
    """
    Write answers into file
    
    :param data: answers after checking 
    :param folder_name: folder path 
    :return: 
    """
    data = json.dumps(data)
    data = json.loads(str(data))
    file_name = os.path.join(folder_name, folder_name + '_answer.json')
    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def control_sequence(massive):
    """
    Control input sequence for correct bool digits (1 and 0) and convert it into list
    
    :param massive: string for control and revert 
    :return: massive_of_bool list with correct bool digits
    """
    massive_of_bool = list(map(int, massive.split()))
    while not set(massive_of_bool).issubset([0, 1]):
        # Control input zone
        print(f"Enter the correct sequence with only 0 or 1!")
        massive_of_bool = list(map(int, input('Enter the sequence of 0 or 1: ').split()))

    return massive_of_bool


def max_count_of_digit(massive_of_bool):
    """
    Counts the maximum length of 1 in the sequence
    
    :param massive_of_bool: clean sequense for cheking
    :return: max_length max count of 1 digits
    """
    # NOT USING
    # USE LOOPS - TOO EASY:)
    only_ones = re.findall(r'[1]+', ''.join(list(map(str, massive_of_bool))))
    if only_ones:
        max_length = len(max(only_ones, key=len))
    else:
        max_length = 0
    print(f"{max_length} – massive is: {massive_of_bool}")

    return max_length


def main():
    # create or clean folder for answers
    folder_name = create_folder_for_answer()
    answer_dict = dict()
    print("Enter 'exit' for exit")

    # Get massive of nums
    massive_of_bool = input('Enter the sequence of 0 or 1: ')
    # massive_of_bool = list(map(int, input('Enter the sequence of 0 or 1: ').split()))

    while massive_of_bool != 'exit':
        # input control
        massive_of_bool = control_sequence(massive_of_bool)
        # maximum length search 
        # USE LOOPS - TOO EASY:)
        only_ones = re.findall(r'[1]+', ''.join(list(map(str, massive_of_bool))))
        max_func = lambda x: len(max(x, key=len)) if x else 0
        max_length = max_func(only_ones)

        print(f"{max_length = } – massive is: {massive_of_bool}")

        # adding totals to the dictionary
        if max_length in answer_dict.keys():
            answer_dict.get(max_length).append(massive_of_bool)
        else:
            answer_dict[max_length] = [massive_of_bool]

        print("\nEnter 'exit' for exit")
        massive_of_bool = input('Enter the sequence of 0 or 1: ')

    # write answer to file in correct form
    write_answers(answer_dict, folder_name)


if __name__ == '__main__':
    try:
        # ALL RPA TECHNOLOGY MUST RUN SMOOTHLY
        main()
    except Exception as e:
        print(f"Something go wrong")
        print(e)
