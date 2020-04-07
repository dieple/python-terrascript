from utils import *
from policy_documents import *
from process_bastion import *
from pprint import pprint

# setup some dynamic required fields
def setup_input_kwargs(module_name, build_data, src_data, mod_data, ts):

    region = build_data["region"]
    workspace = build_data["workspace"]

    input_kwargs = {}

    # module param inputs dynamically generated from input yaml file
    # print(mod_data[workspace]['module']['inputs'])
    for k, v in mod_data[workspace]['module']['inputs'].items():
        input_kwargs[k] = v

    # check if 'name' (key exists) and not populated in the yaml
    # then use the label.id field instead
    if 'name' in input_kwargs:
        if is_empty(input_kwargs["name"]):
            input_kwargs["name"] = "{0}module.{1}.{2}{3}".format("${", "label", "id", "}")  # label.id output

    if 'tags' in input_kwargs:
        if is_empty(input_kwargs["tags"]):
            input_kwargs["tags"] = "{0}module.{1}.{2}{3}".format("${", "label", "tags", "}")  # label.tags output

    if 'region' in input_kwargs:
        if is_empty(input_kwargs["region"]):
            input_kwargs["region"] = region

    if module_name == "vpc":
      pass

    elif module_name == "kms":
        input_kwargs = process_kms(input_kwargs, build_data)

    elif module_name == "ssh-key-pair":
        if is_empty(input_kwargs["key_name"]):
            input_kwargs["key_name"] = "{0}module.{1}.{2}{3}".format("${", "label", "id", "}")  # label.id output

    elif module_name == "bastion":
        _ = process_bastion(input_kwargs, build_data, ts)



    input_kwargs["source"] = src_data[workspace][module_name]

    return input_kwargs

