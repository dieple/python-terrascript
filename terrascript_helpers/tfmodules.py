import os
import fnmatch

from ruamel.yaml import YAML

try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk

from tfprompts import prompt_user



def parse_envs_file(envs_file):
    """
    Load and read in the envs.yaml file
    :param envs_yaml_file: the input yaml file name to read
    :return: the content of the file
    """
    src = YAML(typ='safe')
    with(open(envs_file, 'r')) as env_file:
        env_data = src.load(env_file)
    ws_data_dict = env_data['workspace']

    workspaces = []
    for ws_name, ws_info in ws_data_dict.items():
        # setup the display (workspace|account_id|account_name) for prompting user to select
        ws = "{0}{1}{2}{1}{3}".format(ws_name, "|", ws_data_dict[ws_name]['account_id'], ws_data_dict[ws_name]['account'])
        workspaces.append(ws)
    return workspaces, ws_data_dict


def get_modules_to_run(environment, build_file):
    src = YAML(typ='safe')
    # aws_accounts
    with open(build_file) as f:
        modules_to_run_json = src.load(f)
        modules_to_run_data = modules_to_run_json[environment]
    return modules_to_run_data


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                if  ".terraform" not in os.path.join(root):
                    result.append(os.path.join(root, name))
    return result


def find_modules(dir_names):
    """
    Fetch list of directories (modules) currently supported
    :param dir_names: The name of directory contains all terraform modules
    :return: list of directory modules
    """
    modules_to_build = []
    for dir in dir_names:
        modules_to_build = find('*.yaml', './' + dir)

    return modules_to_build


def prompt_modules(iterable_data):
    """
    Display and prompt user to select module(s) to build
    This is a multi selection enabled prompt.
    :param iterable_data: Modules to select
    :return: Selected module(s)
    """
    modules_options = {"multi": True,
                       "mouse": False,
                       "prompt": "Select component/module to build (shift-tab key for multi-selection):  > "}

    return prompt_user(iterable_data, **modules_options)

