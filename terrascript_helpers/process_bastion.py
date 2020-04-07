import terrascript
import terrascript.data
import terrascript.provider

from utils import is_empty


# setup some dynamic required fields
def process_bastion(input_kwargs, build_data, ts):

  vpc_key = "env:/{}/{}/{}".format(build_data["workspace"], "vpc", "terraform.tfstate")
  ssh_key = "env:/{}/{}/{}".format(build_data["workspace"], "ssh_key_pair", "terraform.tfstate")

  # get the vpc remote state data
  ts += terrascript.data.terraform_remote_state(
                            "vpc",
                            backend="s3",
                            config={"bucket": build_data["bucket"], "key": vpc_key, "region": build_data["bucket_region"], "dynamodb_table": build_data["dynamodb"]}
                            )

  # ssh key pair remote data:
  ts += terrascript.data.terraform_remote_state(
                            "ssh_key_pair",
                            backend="s3",
                            config={"bucket": build_data["bucket"], "key": ssh_key, "region": build_data["bucket_region"], "dynamodb_table": build_data["dynamodb"]}
                            )

  input_kwargs["tags"] = "${module.label.tags}"
  input_kwargs["key_name"] = "${data.terraform_remote_state.ssh_key_pair.outputs.key_name}"
  input_kwargs["vpc_id"] = "${data.terraform_remote_state.vpc.outputs.vpc_id}"
  input_kwargs["public_subnets"] = "${data.terraform_remote_state.vpc.outputs.public_subnets}"
  input_kwargs["environment"] = build_data["environment"]

  # if bastion_name is not enter then use the generate label.id instead
  if is_empty(input_kwargs["bastion_name"]):
    input_kwargs["bastion_name"] = "${module.label.id}"

  # print ("input_kwargs: {0}".format(input_kwargs))
  return input_kwargs

