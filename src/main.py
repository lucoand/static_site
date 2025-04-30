from copy_directory_tree import *
from generate_page import *
import sys

def main():
    basepath = ""
    if len(sys.argv) <= 1:
        basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if basepath == "":
        raise Exception("Something went wrong with arguments")
    destination = "docs"

    copy_directory_tree("static", destination)
    generate_pages_recursive(basepath, "content", "template.html", destination)

main()
