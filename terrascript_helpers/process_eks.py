from utils import is_empty

# setup some dynamic required fields
def process_eks(input_kwargs, build_data):

  # these fields are used in the terraform module to dynamically
  # fetch the vpc and subnets
  input_kwargs["bucket"] = build_data["bucket"]
  input_kwargs["bucket_region"] = build_data["bucket_region"]
  input_kwargs["dynamodb"] = build_data["dynamodb"]
  input_kwargs["workspace"] = build_data["workspace"]

  if is_empty(input_kwargs["cluster_name"]):
    input_kwargs["cluster_name"] = "{0}module.{1}.{2}{3}".format("${", "label", "id", "}")

  return input_kwargs

