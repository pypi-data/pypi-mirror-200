import datetime
import pathlib
import time
import os
import json
import shutil
import subprocess
import unittest


class TestCase(unittest.TestCase):

    maxDiff = None

    @staticmethod
    def get_template(filepath):
        with open(f'{filepath}.template.json') as template:
            return json.load(template)

    def create_cdk_templates(self):
        result = time_it(
            (
                'cdk ls '
                '--no-version-reporting '
                '--no-path-metadata '
                '--no-asset-metadata'
            ),
            function=subprocess.run,
            description=f'cdk ls',
            shell=True,
            capture_output=True,
        )
        print(result.stderr.decode())
        print(result.stdout.decode())
        self.assertEqual(result.returncode, 0)

    def assert_cdk_templates_equal(self, stack_name):
        self.assertEqual(
            self.get_template(f"cdk.out/{stack_name}"),
            self.get_template(f"tests/fixtures/{stack_name}")
        )

    def assert_attributes_equal(self, thing=None, attributes=None):
        self.assertEqual(
            sorted(dir(thing)), sorted(attributes)
        )

    @staticmethod
    def remove_dist():
        try:
            shutil.rmtree('dist')
        except FileNotFoundError:
            'already removed'

    def build_and_publish(self):
        git_push()
        self.remove_dist()
        os.system('python3 -m build')
        self.assertEqual(
            os.system('python3 -m twine upload dist/*'), 0
        )

def logger(message, level="INFO"):
    print(f"[{level}] {message}")

def error(message):
    logger(message, level="ERROR")

def delete(filepath):
    try:
        os.remove(filepath)
    except FileNotFoundError:
        f"Could not find {filepath}"

def file_exists(filepath):
    return pathlib.Path(filepath).exists()

def make_dir(filepath):
    try:
        os.makedirs(pathlib.Path(filepath).parent)
    except FileExistsError:
        pass

def write_config(filepath=None, parser=None):
    "Write Config Parameters to filepath"
    make_dir(filepath)
    with open(filepath, "w") as configfile:
        parser.write(configfile)

def write_file(filepath=None, data=None):
    "Write Credentials to filepath"
    filepath = filepath.replace('\\', '/')
    make_dir(filepath)
    logger(f"Writing data to {filepath}")
    with open(filepath, "w") as writer:
        writer.write(str(data))

def delimiter():
    print("="*80)

def header(environment):
    delimiter()
    print(f"\t[WARNING] You are making changes to the {environment} Environment [WARNING]")
    delimiter()

def log_performance(message):
    performance = f"{datetime.datetime.now()}:{message}\n"
    logs_path = 'tests/logs'
    os.makedirs(logs_path, exist_ok=True)
    with open(f'{logs_path}/performance.log', 'a') as writer:
        writer.write(performance)
    print(performance)

def time_it(*args, function=None, description='run process', **kwargs):
    start_time = time.time()
    result = function(*args, **kwargs)
    log_performance(f'{description}:{time.time() - start_time:.1f}')
    return result

def to_camel_case(text):
    return ''.join(text.title().split('-'))

def get_commit_message():
    return input("Enter commit message: ")

def git_push():
    try:
        update_pyproject_version()
    except FileNotFoundError:
        pass
    finally:
        os.system(f'git commit -am "{get_commit_message()}"')
        os.system('git push')