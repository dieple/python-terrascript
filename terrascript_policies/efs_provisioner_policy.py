from awacs.aws import Action, Allow, PolicyDocument, Principal, Statement
from awacs.iam import ARN as IAM_ARN
import awacs.elasticfilesystem as elasticfilesystem


# setup some dynamic required fields
def efs_policy_document(input_kwargs, build_data):

  user = "root"
  account = build_data["account_id"]

  pd = PolicyDocument(
    Version="2012-10-17",
    Id="EFS-Permissions",
    Statement=[
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          elasticfilesystem.DescribeFileSystems,
          elasticfilesystem.CreateFileSystem,
          elasticfilesystem.CreateTags,
          elasticfilesystem.DescribeMountTargets,
          elasticfilesystem.CreateMountTarget
        ],
        Resource=['*']
      )
    ]
  )


  input_kwargs["policy"] = pd.to_json()

  return input_kwargs
