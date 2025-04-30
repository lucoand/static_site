import os
from markdown_to_html import *

def generate_page(basepath: str, from_path: str, temlate_path: str, dest_path):
    if not os.path.exists(from_path):
        raise Exception(f"Source markdown file {from_path} does not exist!  Aborting!")
    if not os.path.exists(temlate_path):
        raise Exception(f"Template {temlate_path} does not exist! Aborting!")
    # if not os.path.exists(dest_path):
    #     print(f"Generating destination {dest_path}")
    #     os.mkdir(dest_path)
    destination_directory_tree = os.path.split(dest_path)
    if destination_directory_tree[0] == "" and destination_directory_tree[1] == "":
        raise Exception(f"No destination path given!  Should be given as destination/path/file")
    if destination_directory_tree[1] == "":
        raise Exception(f"Invalid destination path!  Must point to a file name")
    if destination_directory_tree[0] != "":
        generate_destination_directory(destination_directory_tree[0])
    if os.path.exists(dest_path):
        print(f"File already exists at {dest_path}.  Overwriting.")

    print(f"Generating page from {from_path} to {dest_path} using {temlate_path}")
    md = ""
    with open(from_path, 'r') as file:
        md = file.read()
    # print(md)
    template = ""
    with open(temlate_path, 'r') as file:
        template = file.read()
    # print(template)
    node = markdown_to_html_node(md)
    html = node.to_html()
    title = extract_title(md)
    # print(title)
    # print(html)
    template_list = template.split("{{ Title }}")
    template = template_list[0] + title + template_list[1]
    # print(template)
    template_list = template.split("{{ Content }}")
    template = template_list[0] + html + template_list[1]
    template = basepath_correction(basepath, template)
    print("Markdown converted to HTML.")
    print(f"Writing HTML to {dest_path}")
    with open(dest_path, 'w') as file:
        file.write(template)
    print(f"Success!")

def basepath_correction(basepath: str, html: str) -> str:
    if basepath == "/":
        return html
    html = find_replace(html, 'href="/', f'href="{basepath}')
    html = find_replace(html, 'src="/', f'src="{basepath}')
    return html

def find_replace(string: str, old_substring: str, new_substring: str) -> str:
    temp = string.split(old_substring)
    string = new_substring.join(temp)
    return string

def generate_destination_directory(path: str):
    pathname = os.path.split(path)
    if pathname[0] == "":
        if not os.path.exists(pathname[1]):
            os.mkdir(pathname[1])
        return
    generate_destination_directory(pathname[0])
    if not os.path.exists(path):
        os.mkdir(path)
    return
    

def generate_pages_recursive(basepath: str, dir_path_content: str, template_path: str, dest_dir_path: str):
    file_list = os.listdir(dir_path_content)
    # print(f"{file_list}")
    for file in file_list:
        file_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(file_path):
            dest_path = dest_path[:-2] + "html"
            generate_page(basepath, file_path, template_path, dest_path)
            # print(f"Source Path: {file_path}")
            # print(f"Destination Path: {dest_path}")
            continue
        generate_pages_recursive(basepath, file_path, template_path, dest_path)
    return



