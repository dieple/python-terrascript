from awacs.aws import Action, Allow, PolicyDocument, Principal, Statement
from awacs.iam import ARN as IAM_ARN
import awacs.logs as logs
import awacs.ec2 as ec2
import awacs.ce as ce
import awacs.events as events
import awacs.secretsmanager as secretsmanager
import awacs.rds as rds

# addtional_policy_arns:
# - "arn:aws:iam::aws:policy/service-role/AWSLambdaKinesisExecutionRole"
# - "arn:aws:iam::aws:policy/service-role/AWSLambdaDynamoDBExecutionRole"
# - "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
# - "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
# #        - "arn:aws:iam::aws:policy/service-role/AWSXrayWriteOnlyAccess"

# setup some dynamic required fields
def codebuild_policy_document(input_kwargs, build_data):

  user = "root"
  account = build_data["account_id"]
  region =  build_data["region"]
  logs_arn =  f"arn:aws:logs:{region}:{account}:log-group:/aws/lambda/*"
  ec2_arn = ["arn:aws:s3:::product-images-*", "arn:aws:s3:::product-images-*/*"]

  pd = PolicyDocument(
    Version="2012-10-17",
    Id="Lambda-Common-Permissions",
    Statement=[
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          logs.CreateLogStream,
          logs.PutLogEvents
        ],
        Resource=[logs_arn]
      ),
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          ec2.CreateNetworkInterface,
          ec2.DescribeNetworkInterfaces,
          ec2.DeleteNetworkInterface,
          "ec2:Describe*",
          ec2.CreateSnapshot,
          ec2.DeleteSnapshot,
          ec2.CreateImage,
          ec2.CopyImage,
          ec2.DeregisterImage,
          ce.GetCostAndUsage,
          events.EnableRule,
          secretsmanager.GetSecretValue,
          secretsmanager.DescribeSecret,
          "kms:*",
          "cloudwatch:*",
          "s3:*"
        ],
        Resource=ec2_arn
      ),
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          rds.DescribeDBClusterSnapshots,
          rds.DescribeDBClusters,
          rds.CopyDBClusterSnapshot,
          rds.ModifyDBClusterSnapshotAttribute,
          rds.ListTagsForResource
        ],
        Resource=['*']
      )
    ]
  )


  input_kwargs["policy"] = pd.to_json()

  return input_kwargs
