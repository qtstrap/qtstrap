import sys
import click
from pathlib import Path
import shutil
from PyInquirer import prompt, print_json, Separator
import uuid
import os


@click.group()
def main():
    pass


def validate_name(answer):
    if len(answer) == 0:
        return "name can't be empty"
    if " " in answer:
        return "name can't contain spaces"
    return True


init_prompt = [
    {
        'type': 'input',
        'name': 'app_name',
        'message': 'Application Name:',
        'validate': validate_name,
    },
    {
        'type': 'input',
        'name': 'app_publisher',
        'message': 'Publisher Name:',
        'validate': validate_name,
    },
]


@main.command()
def init():
    parent = Path(__file__).parent 
    template = Path(parent / 'template')
    template_files = template.rglob('*')
    
    if not Path('project.ini').exists():
        result = prompt(init_prompt)
        if result:
            with open('project.ini', 'w') as f:
                f.write(f'AppName = {result["app_name"]}\n')
                f.write(f'AppVersion = 0.1\n')
                f.write(f'AppPublisher = {result["app_publisher"]}\n')
                f.write(f'AppExeName = {result["app_name"]}.exe\n')
                f.write('AppIconName = resources/application.ico\n')
                guid = '{{' + str(uuid.uuid4()) + '}'
                f.write(f'AppId = {guid}\n')

    for f in template_files:
        dest = f.relative_to(template)
        if not dest.exists():
            if f.is_dir():
                Path.mkdir(dest)
            if f.is_file():
                shutil.copy(f, dest)
                # print(f'copying {dest}')
        # else:
        #     print(f'skipping {dest}')


@main.command()
def run():
    print('run')


@main.command()
def build():
    print('build')

