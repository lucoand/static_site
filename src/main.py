from copy_directory_tree import *
from generate_page import *


def main():
    copy_directory_tree("static", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

main()
