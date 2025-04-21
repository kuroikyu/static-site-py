from markdown import gerenate_pages_recursive
from utils import copy_static_to_public


def main():
    copy_static_to_public()
    gerenate_pages_recursive("./content", "./template.html", "./public")


main()
