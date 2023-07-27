from awacs.aws import Action, Allow, PolicyDocument, Principal, Statement
from awacs.iam import ARN as IAM_ARN
import awacs.elasticfilesystem as elasticfilesystem

def create_efs_policy_document(build_data):
    user = "root"
    account_id = build_data["account_id"]

    # Create the policy statement
    efs_statement = Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account_id)]),
        Action=[
            elasticfilesystem.DescribeFileSystems,
            elasticfilesystem.CreateFileSystem,
            elasticfilesystem.CreateTags,
            elasticfilesystem.DescribeMountTargets,
            elasticfilesystem.CreateMountTarget
        ],
        Resource=['*']
    )

    # Create the policy document
    efs_policy_document = PolicyDocument(
        Version="2012-10-17",
        Id="EFS-Permissions",
        Statement=[efs_statement]
    )

    return efs_policy_document.to_json()

# Example usage:
input_kwargs = {}
build_data = {"account_id": "123456789012"}  # Replace with the actual account ID
policy_json = create_efs_policy_document(build_data)
input_kwargs["policy"] = policy_json
