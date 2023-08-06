import pyperclip
import os

def load_template(template_name):
    curr_path = os.path.dirname(__file__)
    file_path = os.path.join(curr_path, './' + template_name + '.py')
    template_code = ""
    with open(file_path, 'r') as f:
        template_code = f.read()

    f.close()
    pyperclip.copy(template_code)
    return template_code

def list_available_templates():
    arr = []
    print(os.listdir())
    arr.append('union_find')
    arr.append('trie')
    print(arr)
    return arr