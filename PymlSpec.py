import testinfra
import sys
import yaml
import shutil
import platform
import time
BACKEND = {"local", "docker", "podman", "ssh",
           "salt", "kubectl", "openshift", "winrm"}
TEST_ITEMS = {"module", "content"}
total_error = 0
total_success = 0
total_tests = 0


class Color:
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'


class PymlError(Exception):
    pass


class UnexpectedArgumentError(Exception):
    pass


def print_success(text):
    print(f'{Color.GREEN}{text}', end="")
    print(f'{Color.RESET}', end="")


def print_error(text):
    print(f'{Color.RED}{text}', end="")
    print(f'{Color.RESET}', end="")


width = 0


def print_delimiter(text: str, color=Color.RESET):
    terminal_size = shutil.get_terminal_size()
    text = "  " + text + "  "
    global width
    width = terminal_size.columns
    local_width = int((width - len(text)) / 2)
    print(f'{color}', end="")
    for i in range(local_width):
        print("=", end="")
    print(text, end="")
    for i in range(local_width):
        print("=", end="")
    print(f'{Color.RESET}')


def test_execute(title, host, module, args, content, expect, backend, content_args):
    start = time.time()
    module_result = eval(f"host.{module}('{args}')")
    if content_args == None:
        content_result = eval(f"module_result.{content}")
    else:
        content_result = eval(f"module_result.{content}('{content_args}')")
    try:
        assert content_result == expect
        print_delimiter(title)
        print("\n")
        print_success("Success\n")
        global total_success
        total_success += 1
    except AssertionError as e:
        print_delimiter(title, color=Color.RED)
        print(f'{Color.RED}', end="")
        print("\n")
        print("Error")
        print(f"Expect value {expect}, but actually {content_result}")
        global total_error
        total_error += + 1
    print(f"Coverage {total_success}/{total_tests}")
    print(f"Test proceed in {time.time() - start:.1g}s")
    print(f'{Color.RESET}', end="")
    return


def parse_file(file: dict):
    for host in file:
        if "tests" not in file[host]:
            raise PymlError(f"yaml must contain tests key in {file['host']}")
        if file[host]["backend"].split(":")[0] not in BACKEND:
            raise PymlError(
                f"yaml backend key must contain {BACKEND} but got {file[host]['backend']} in {file[host]}")
        connection = testinfra.get_host(file[host]["backend"])
        for test in file[host]["tests"]:
            for key in test.keys():
                test_keys = {i for i in test[key]}
                if not TEST_ITEMS.issubset(test_keys):
                    raise PymlError(
                        f"test must have 2 keys module, content.\n but got {test_keys} in {file['host']} ")
                if "expect" not in test_keys:
                    test[key]["expect"] = True
                if "args" not in test_keys:
                    test[key]["args"] = ""
                if "content_args" not in test_keys:
                    test[key]["content_args"] = None
                test_execute(key, connection, module=test[key]["module"], args=test[key]
                             ["args"], content=test[key]["content"], expect=test[key]["expect"], backend=file[host]["backend"], content_args=test[key]["content_args"])
    return


def calc_num_of_schedule(file) -> int:
    num_of_schedule = 0
    for host in file:
        if "tests" not in file[host]:
            raise PymlError(f"yaml must contain tests key in {file['host']}")
        num_of_schedule = num_of_schedule + len(file[host]["tests"])
    return num_of_schedule


def read_yaml(file_name: str) -> dict:
    with open(file_name, 'r') as yml:
        FILE = yaml.safe_load(yml)
    return FILE


if __name__ == '__main__':
    start = time.time()
    if len(sys.argv) != 2:
        raise UnexpectedArgumentError("must have 1 argument")
    FILE = read_yaml(sys.argv[1])
    print_delimiter("test information")
    print(f"platform {platform.system()} version {platform.version()}")
    print(
        f"Python version {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")
    total_tests = calc_num_of_schedule(FILE)
    print(f"scheduled tests {total_tests}")
    print("", end="\n\n")
    print_delimiter("start test", color=Color.BLUE)
    parse_file(FILE)
    color = Color.GREEN if total_success == total_tests else Color.RED
    print_delimiter(f"Test Ended in {time.time() - start:.1g}s", color=color)
    print(
        f"OK={total_success}, NG={total_error}, Total={total_tests}".rjust(width))
