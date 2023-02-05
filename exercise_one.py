import os
import json
import shutil


def check_bracket(text):
    """
    Function for tracking closed bracket
    
    :param :text :text for scanning
    :return: string with True or False
    """
    counter = text.count('(')
    counter_2 = text.count(')')
    if counter == counter_2:
        print(f"True")
        return f"True"
    else:
        print(f"False")
        return f"False"


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
    file_name = os.path.join(folder_name, folder_name + '_answer.json' )
    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    # create or clean folder for answers
    folder_name = create_folder_for_answer()
    
    print("Enter 'exit' for exit")
    text = input(f'Enter your string: ')
    answer_dict = dict()

    while text != 'exit':
        scanning_text = list(text)
        answer = check_bracket(scanning_text)
        if answer in answer_dict.keys():
            answer_dict.get(answer).append(text)
        else:
            answer_dict[answer] = [text]
        print("\nEnter 'exit' for exit")
        text = input(f'Enter your string: ')
        
    # write answer to file in correct form
    write_answers(answer_dict, folder_name)


if __name__ == '__main__':
    try:
        # ALL RPA TECHNOLOGY MUST RUN SMOOTHLY
        main()
    except Exception as e:
        print(f"Something go wrong")
        print(e)