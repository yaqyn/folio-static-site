import os
import shutil
import sys

from markdown_to_html import extract_title, generate_page


def copy_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    for name in os.listdir(source):
        source_path = os.path.join(source, name)
        destination_path = os.path.join(destination, name)
        if os.path.isfile(source_path):
            print(f"Copying {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            copy_directory(source_path, destination_path)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_directory("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


def generate_pages_recursive(dir_path, template_path, dest_dir_path, basepath="/"):
    for name in os.listdir(dir_path):
        source_path = os.path.join(dir_path, name)
        destination_path = os.path.join(dest_dir_path, name)
        if os.path.isdir(source_path):
            os.makedirs(destination_path, exist_ok=True)
            generate_pages_recursive(
                source_path, template_path, destination_path, basepath
            )
        elif name.endswith(".md"):
            destination_path = os.path.join(
                dest_dir_path, name.removesuffix(".md") + ".html"
            )
            generate_page(source_path, template_path, destination_path, basepath)

main()
