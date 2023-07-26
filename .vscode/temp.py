# final 04 July 2023 11:20
# This is for creating vs code snippets from the markdown files
# just provide the base folder containing the markdown files and place the generated cpp.code-snippets and py.code-snippets files in the .vscode folder

import os
import re
import json

vscode_snippets={}

counter = 1 # global counter for handling key colliding

# final

def return_array(code):
    """
    return body of the vscode snippet as array of strings
    """
    separated_snippet = code.split("\n")
    new_snippet = [line for line in separated_snippet]
    return new_snippet


def extract_code_blocks_with_headings(file_path):
    """
    extract the code blocks and the heading before it from the markdown file for forming the vscode snippets
    """
    with open(file_path, "r") as file:
        content = file.read()

    # Regular expression pattern to match headings, code blocks, and language
    pattern = (
        r"#{1,6}(.*?)\n\s*(.*?)\s*(`{3}|~{3})(.*?)\n\s*(.*?)\s*(`{3}|~{3})"
    )

    matches = re.findall(pattern, content, re.DOTALL)

    # ad
    code_blocks_with_headings = matches
    # Print the extracted headings, code blocks, and language
    for heading, desc, _, language, code, _ in code_blocks_with_headings:
        # split_string = heading.split('\n', 1)
        # heading = split_string[0]
        # rest_of_string = split_string[1] if len(split_string) > 1 else heading

        global vscode_snippets
        if vscode_snippets.get(heading) is not None:
            global counter
            heading = heading + str(counter)
            counter += 1
        vscode_snippets[heading] = {}
        vscode_snippets[heading]["prefix"] = heading
        vscode_snippets[heading]["description"] = desc
        match language:
            case "cpp":
                vscode_snippets[heading]["scope"]="cpp, c"
            case "py":
                vscode_snippets[heading]["scope"]="python"
            case "java":
                vscode_snippets[heading]["scope"]="java"
            case "html":
                vscode_snippets[heading]["scope"]="html, javascript, typescript"
            case "js":
                vscode_snippets[heading]["scope"]="html, javascript, typescript"
                
        vscode_snippets[heading]["body"] = return_array(code)    
            
        


def get_file_extension(file_path):
    """
    get the file extension
    """
    _, extension = os.path.splitext(file_path)
    return extension


def get_folders_and_files(base_folder):
    """
    get the folders and files in a base folder
    """

    folders = []
    files = []

    for root, dirs, filenames in os.walk(base_folder):
        for directory in dirs:
            folders.append(os.path.join(root, directory))
        for filename in filenames:
            files.append(os.path.join(root, filename))

    for file in files:
        ext = get_file_extension(file)
        if ext == ".md":
            extract_code_blocks_with_headings(file)

    for folder in folders:
        get_folders_and_files(folder)



BASE_FOLDER=r'C:\Users\adity\Desktop\Snippets\Web Development'

print('creating vscode snippets')
print('from the BASE_FOLDER : '+BASE_FOLDER)
current_folder = os.getcwd()
print("To the current folder : ", current_folder)

get_folders_and_files(BASE_FOLDER)

with open("ad_vscode_snippets.code-snippets", "w") as f:
    json.dump(vscode_snippets, f, indent=2)


# a=input('Press Enter to close this terminal')


