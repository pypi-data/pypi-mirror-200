import argparse
from rich import print
from pick import pick


def cli():
    parser = argparse.ArgumentParser(description="用于快速创建PyPI包模板")
    subparsers = parser.add_subparsers(title="Awa2", metavar="Command")

    quickstart_parser = subparsers.add_parser("quickstart", help="快速开始：根据输入信息创建模板")
    quickstart_parser.set_defaults(handle=handle_quickstart)

    quickupload_parser = subparsers.add_parser("quickupload", help="快速发布：打包并发布库入Pypi")
    quickupload_parser.set_defaults(handle=handle_quickupload)

    args = parser.parse_args()
    if hasattr(args, 'handle'):
        args.handle(args)
    else:
        parser.print_help()


def handle_quickstart(args):
    print("[bold white]Please entry library info[/bold white] :grinning_face_with_smiling_eyes:")

    print("[[bold blue]Project Name[/bold blue]]", end="")
    project_name = input(" : ")
    if project_name == "":
        project_name = "Awa2"

    print("[[bold blue]Setup Tool[/bold blue]]", end="")
    project_setuptool = pick(("setup.py", "pyproject.toml"), "Choose your project setup tool", indicator="->",
                             default_index=1
                             )
    print(" : " + project_setuptool[0])

    print("[[bold blue]Description[/bold blue]]", end="")
    project_description = input(" : ")
    if project_description == "":
        project_description = "Simple Setup"

    print("[[bold blue]Version[/bold blue]]", end="")
    project_version = input(" : ")
    if project_version == "":
        project_version = "1.0.0"

    print("[[bold blue]Author[/bold blue]]", end="")
    project_author = input(" : ")
    if project_author == "":
        project_author = "XiangQinxi"

    print("[[bold blue]Layout[/bold blue]]", end="")
    project_layout = pick(("SRC Layout", "Flat Layout"), "Choose your project layout", indicator="->", default_index=1)
    print(" : " + project_layout[0])

    open("README.md", "w+", encoding="utf-8").write(f"# {project_name} \n \n> setup by awa2")

    from os import mkdir
    from os.path import exists
    if project_layout[0] == "Flat Layout":
        if not exists(f"./{project_name}"):
            mkdir(f"./{project_name}")
        if not exists(f"./{project_name}/__init__.py"):
            open(f"./{project_name}/__init__.py", "w+").write("print('Hello awa2')")
    elif project_layout[0] == "SRC Layout":
        if not exists(f"./src"):
            mkdir(f"./src")
        if not exists(f"./src/{project_name}"):
            mkdir(f"./src/{project_name}")
        if not exists(f"./src/{project_name}/__init__.py"):
            open(f"./src/{project_name}/__init__.py", "w+").write("print('Hello awa2')")

    if project_setuptool[0] == "setup.py":
        if not exists("setup.py"):
            with open("setup.py", "w+") as setup:
                if project_layout[0] == "Flat Layout":
                    layout = "find_packages(where='.'),"
                elif project_layout[0] == "SRC Layout":
                    layout = "find_packages(where='src'),\npackage_dir={'': 'src'},"
                code = f"""
from setuptools import find_packages, setup

setup(
    name="{project_name}",
    version="{project_version}",
    author="{project_author}",
    description="{project_description}",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3",
    packages={layout}
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
                """
                setup.write(code)
    elif project_setuptool[0] == "pyproject.toml":
        if not exists("pyproject.toml"):
            with open("pyproject.toml", "w+") as setup:
                import toml
                code_toml = {
                        "project": {
                            "name": project_name,
                            "version": project_version,
                            "authors": [{"name": project_author}],
                            "description": project_description,
                            "readme": "README.md",
                        },
                        "options": {
                            "packages": "find:"
                        }
                }
                code_toml["options"]["package_dir"] = "src"
                code = toml.dumps(code_toml)
                setup.write(code)
        print("[bold blue]Setup Code[/bold blue] : ")
        print(code)


def handle_quickupload(args):
    from os import system
    from sys import executable
    system(f"{executable} -m build")
    system(f"{executable} -m twine upload dist/*")


if __name__ == '__main__':
    cli()
