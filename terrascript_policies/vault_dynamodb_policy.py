from awacs.aws import Action, Allow, PolicyDocument, Principal, Statement
from awacs.iam import ARN as IAM_ARN
import awacs.dynamodb as dynamodb
import awacs.kms as kms

# addtional_policy_arns:
# "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"

# setup some dynamic required fields
def codebuild_policy_document(input_kwargs, build_data):

  user = "root"
  account = build_data["account_id"]
  region =  build_data["region"]
  table_name =  build_data["table_name"]
  db_arn = f"arn:aws:dynamodb:{region}:${account}:table/${table_name}"

  ec2_arn = ["arn:aws:kinesis:*:*:stream/aws-rds-das-*"]

  pd = PolicyDocument(
    Version="2012-10-17",
    Id="Dynamodb-Permissions",
    Statement=[
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          dynamodb.DescribeLimits,
          dynamodb.DescribeTimeToLive,
          dynamodb.ListTagsOfResource,
          dynamodb.DescribeReservedCapacityOfferings,
          dynamodb.DescribeReservedCapacity,
          dynamodb.ListTables,
          dynamodb.BatchGetItem,
          dynamodb.BatchWriteItem,
          dynamodb.CreateTable,
          dynamodb.DeleteItem,
          dynamodb.GetItem,
          dynamodb.GetRecords,
          dynamodb.PutItem,
          dynamodb.Query,
          dynamodb.UpdateItem,
          dynamodb.Scan,
          dynamodb.DescribeTable
        ],
        Resource=[db_arn]
      ),
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          kms.Encrypt,
          kms.Decrypt,
          kms.DescribeKey
        ],
        Resource=["*"]
      )
    ]
  )


  input_kwargs["policy"] = pd.to_json()

  return input_kwargs
