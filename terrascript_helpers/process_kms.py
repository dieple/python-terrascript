from kms_policy import kms_policy_document


# setup some dynamic required fields
def process_kms(input_kwargs, build_data):

  # aws policy statements is a bit tricky to specify in the yaml file so required special processing here.
  # input_kwargs["policy"]
  input_kwargs = kms_policy_document(input_kwargs, build_data)

  # print ("input_kwargs: {0}".format(input_kwargs))
  return input_kwargs

