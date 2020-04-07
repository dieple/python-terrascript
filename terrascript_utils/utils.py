import copy
import terrascript
import terrascript.provider

from ruamel.yaml import YAML

def get_value(listOfDicts, key):
  for subVal in listOfDicts:
    if key in subVal:
      return subVal[key]

def is_empty(chk_data):
  if chk_data:
    return False
  else:
    return True


def get_yaml_input(module_name, build_data):

  src = YAML(typ='safe')

  # global.yaml
  with open(build_data['varfiles'][0]) as fp:
    global_data = src.load(fp)

  # source.yaml
  with open(build_data['varfiles'][1]) as fsrc:
    src_data = src.load(fsrc)

  # labels
  with open(build_data['varfiles'][2]) as lsrc:
    label_data = src.load(lsrc)

  mod_list = [ m for m in build_data["modules"] if module_name + '.yaml' in m ]
  mod_file_path =  mod_list[0]
  with open(mod_file_path) as fmod:
    mod_data = src.load(fmod)

  return  global_data, src_data, label_data, mod_data


def get_label(module_name, src_data, labels_data, build_data):

  workspace = build_data["workspace"]

  # tags and label
  label_kwargs = {}
  # source.yaml: label: "git::https://github.com/dieple/terraform-modules-012x.git//tagging-label"
  label_kwargs["source"] = src_data[workspace]['label']

  # loop thru labels.yaml file and setup accordingly...
  for k, v in labels_data[workspace].items():
    label_kwargs[k] = v

  if is_empty(label_kwargs["attributes"]):
    label_kwargs["attributes"] = [module_name]

  label = terrascript.Module(_name="label", **label_kwargs)

  return label, label_kwargs


def generate_terraform_backend_provider_and_label(module_name, build_data, ts, add_backend=True):

  backend_data_dict = {}
  terraform_data_dict = {}
  providers_data_dict = {}

  global_data, src_data, labels_data, mod_data = get_yaml_input(module_name, build_data)

  # backend
  workspace = build_data['workspace']
  backend_data_dict["encrypt"] = global_data['terraform']['backend']['encrypt']
  # backend_data_dict["type"] = global_data['terraform']['backend']['type']
  backend_data_dict["region"] = build_data['bucket_region']
  backend_data_dict["bucket"] = build_data['bucket']
  backend_data_dict["dynamodb_table"] = build_data['dynamodb']
  backend_data_dict["key"] = f"{module_name}/terraform.tfstate"

  # providers
  terraform_data_dict["required_version"] = global_data['terraform']['required_version']

  # workspace_iam_role_arn = "arn:aws:iam::{0}:role/administrator".format(build_data["account_id"])
  workspace_iam_role_arn = build_data["workspace_iam_role"]
  providers_data_dict["allowed_account_ids"] = [build_data["account_id"]]
  providers_data_dict["region"] = build_data['region']
  providers_data_dict["version"] = global_data['provider']['aws']['version']

  share_r53_iam_role = build_data["share_r53_iam_role"]

  providers_data_alias_dict = copy.deepcopy(providers_data_dict)
  alias_account_id = share_r53_iam_role.split(':')[-2]
  providers_data_alias_dict["allowed_account_ids"] = [alias_account_id]
  providers_data_alias_dict["alias"] = "share_r53_iam_role"

  if add_backend:
    s3_backend = terrascript.Backend("s3", **backend_data_dict)
    ts += terrascript.Terraform(required_version=terraform_data_dict['required_version'], backend=s3_backend)
  else:
    ts += terrascript.Terraform(required_version=terraform_data_dict['required_version'])

  ts += terrascript.provider.aws(assume_role={"role_arn": workspace_iam_role_arn}, **providers_data_dict)
  ts += terrascript.provider.aws(assume_role={"role_arn": share_r53_iam_role}, **providers_data_alias_dict)
  # TODO: add the rest of providers here.

  label, label_kwargs = get_label(module_name, src_data, labels_data, build_data)
  ts += label

  return ts, label, label_kwargs

