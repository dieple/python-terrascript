#! /usr/bin/env python
import os
import argparse
import sys
import inspect

DIR_LIST = ["terrascript_utils", "terrascript_vars", "terrascript_helpers", "terraform_helpers", "terrascript_policies","components", "generated"]

# realpath() will make your script run, even if you symlink it :)
build_dir = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if build_dir not in sys.path:
  sys.path.insert(0, build_dir)

# include utils or lib modules from a subfolder
for include_dir in DIR_LIST:
  build_subdir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], include_dir)))
  if build_subdir not in sys.path:
    sys.path.insert(0, build_subdir)

# from tfregions import Regions
from tfmodules import prompt_modules, parse_envs_file, find_modules
from tfprompts import prompt_account, prompt_tfaction
from tf_gen_run import tf_generate_and_run

TF_ACTIONS = ["apply", "apply-destroy", "plan", "plan-destroy"]
MODULE_DIRS = ["components"]
ENVS_YAML_FILE = "./terrascript_vars/envs.yaml"
VARFILES_LIST = ["./terrascript_vars/global.yaml", "./terrascript_vars/source.yaml", "./terrascript_vars/labels.yaml"]


def process_arguments():
  """
  Processing user input arguments
  :return: the parsed user input args
  """
  parser = argparse.ArgumentParser()
  optional = parser._action_groups.pop()
  required = parser.add_argument_group('Required arguments')
  optional.add_argument('-i', '--interactive', help='Interactive mode?', required=False, default=True)
  optional.add_argument('-p', '--approve', help='Auto approve?', required=False, default=False)
  optional.add_argument('-v', '--varfiles', help='List of Vars file names', required=False, default=VARFILES_LIST)
  parser._action_groups.append(optional)
  return parser.parse_args()


if __name__ == '__main__':
  args = process_arguments()

  if args.interactive:
    workspaces, workspaces_dict = parse_envs_file(ENVS_YAML_FILE)

    # prompt user to select an account to build
    account_sel = prompt_account(workspaces)
    if account_sel is None:
      print("User abort exiting...")
      exit (1)

    workspace_selected = account_sel.split('|')[0]

    # prompt user to select module(s) to build
    build_modules = prompt_modules(find_modules(MODULE_DIRS))
    if build_modules is None:
      print("User abort exiting...")
      exit (1)

    # prompt user to choose terraform action
    tfaction = prompt_tfaction(TF_ACTIONS)
    if tfaction is None:
      print("User abort exiting...")
      exit (1)

    # setup build data for tf_gen_run.py
    build_data = {}
    build_data = workspaces_dict[workspace_selected]
    build_data["gen_path"] = "generated"
    build_data["workspace"] = workspace_selected
    build_data["modules"] = build_modules
    build_data["auto_approve"] = args.approve
    build_data["interactive"] = args.interactive
    build_data["tfaction"] = tfaction
    build_data["varfiles"] = VARFILES_LIST

    tf_generate_and_run(build_data)
  else:
    pass # CI/CD implement later


