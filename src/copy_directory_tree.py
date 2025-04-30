import os
import shutil

def copy_directory_tree(src: str, dst: str):
    if not os.path.exists(src):
        raise Exception(f"{src} directory missing")

    if os.path.exists(dst):
        shutil.rmtree(dst)
        print(f"removed {dst} directory")
    os.mkdir(dst)
    print(f"created new {dst} directory")

    copy_file(src, dst)


def copy_file(src: str, dst: str):
    file_list = os.listdir(src)
    for file in file_list:
        file_path = os.path.join(src, file)
        destination_path = os.path.join(dst, file)
        if os.path.isfile(file_path):
            copied_file = shutil.copy(file_path, destination_path)
            print(f"{file_path} copied to {copied_file}")
            continue
        os.mkdir(destination_path)
        print(f"created directory {destination_path}")
        copy_file(file_path, destination_path)


