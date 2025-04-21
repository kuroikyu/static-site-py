import os
from pathlib import Path
from blocks import markdown_to_html_node


def extract_title(markdown: str):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()

    raise Exception("No H1 was found in the markdown document")


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}.")

    source_file = open(from_path, "r", encoding="utf-8")
    source_content = source_file.read()
    source_file.close()

    template_file = open(template_path, "r", encoding="utf-8")
    template_content = template_file.read()
    template_file.close()

    page_content = markdown_to_html_node(source_content).to_html()
    page_title = extract_title(source_content)

    template_content = template_content.replace("{{ Title }}", page_title)
    template_content = template_content.replace("{{ Content }}", page_content)

    # Ensure full path exists before running!
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    page_file = open(dest_path, "w", encoding="utf-8")
    page_file.write(template_content)
    page_file.close()


def gerenate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    entries = os.listdir(dir_path_content)

    for entry in entries:
        entry_path = Path(dir_path_content, entry)
        if entry_path.is_file():
            generate_page(entry_path, template_path,
                          Path(dest_dir_path, entry.replace(".md", ".html")))
        else:
            gerenate_pages_recursive(
                entry_path, template_path, Path(dest_dir_path, entry))
