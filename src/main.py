from markdown import gerenate_pages_recursive
from utils import copy_static_to_directory
import sys


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_static_to_directory("docs")
    gerenate_pages_recursive(
        "./content", "./template.html", "./docs", basepath=basepath)


main()
