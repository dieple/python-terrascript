from awacs.aws import Action, Allow, PolicyDocument, Principal, Statement
from awacs.iam import ARN as IAM_ARN
import awacs.logs as logs
import awacs.kinesis as kinesis

# addtional_policy_arns:
# "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"

# setup some dynamic required fields
def codebuild_policy_document(input_kwargs, build_data):

  user = "root"
  account = build_data["account_id"]
  region =  build_data["region"]
  logs_arn =  ["arn:aws:logs:*:*:log-group:/aws/rds/*:log-stream:*", "arn:aws:logs:*:*:log-group:/aws/docdb/*:log-stream:*", "arn:aws:logs:*:*:log-group:/aws/neptune/*:log-stream:*"]
  ec2_arn = ["arn:aws:kinesis:*:*:stream/aws-rds-das-*"]

  pd = PolicyDocument(
    Version="2012-10-17",
    Id="RDS-Monitoring-Permissions",
    Statement=[
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          logs.CreateLogDelivery,
          logs.GetLogDelivery,
          logs.UpdateLogDelivery,
          logs.DeleteLogDelivery,
          logs.ListLogDeliveries
        ],
        Resource=[logs_arn]
      ),
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          kinesis.CreateStream,
          kinesis.PutRecord,
          kinesis.PutRecords,
          kinesis.DescribeStream,
          kinesis.SplitShard,
          kinesis.MergeShards,
          kinesis.DeleteStream,
          kinesis.UpdateShardCount
        ],
        Resource=["arn:aws:kinesis:*:*:stream/aws-rds-das-*"]
      )
    ]
  )


  input_kwargs["policy"] = pd.to_json()

  return input_kwargs
