from utils import is_empty
from process_kms import process_kms
from process_bastion import process_bastion
from process_eks import process_eks

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

    if module_name == "kms":
        input_kwargs = process_kms(input_kwargs, build_data)

    elif module_name == "ssh_key_pair":
        if is_empty(input_kwargs["key_name"]):
            input_kwargs["key_name"] = "{0}module.{1}.{2}{3}".format("${", "label", "id", "}")  # label.id output

    elif module_name == "route53_cross_accounts_zone_and_records":
        if is_empty(input_kwargs["bucket_region"]):
            input_kwargs["bucket_region"] = build_data["bucket_region"]
        if is_empty(input_kwargs["share_r53_iam_role"]):
            input_kwargs["share_r53_iam_role"] = build_data["share_r53_iam_role"]
        if is_empty(input_kwargs["workspace_iam_role"]):
            input_kwargs["workspace_iam_role"] = build_data["workspace_iam_role"]

    elif module_name == 'bastion':
        input_kwargs = process_bastion(input_kwargs, build_data, ts)

    elif module_name == 'dynamodb':
       pass # not much to process with this module but put here to indicate order of build

    elif module_name == 'eks':
        input_kwargs = process_eks(input_kwargs, build_data)

    elif module_name == 'iam_roles_eks_service_accounts':
        if is_empty(input_kwargs["hosted_zone_id"]):
            input_kwargs["hosted_zone_id"] = "*"
        input_kwargs["bucket"] = build_data["bucket"]
        input_kwargs["bucket_region"] = build_data["bucket_region"]
        input_kwargs["workspace"] = build_data["workspace"]
        input_kwargs["dynamodb"] = build_data["dynamodb"]




    input_kwargs["source"] = src_data[workspace][module_name]

    return input_kwargs

