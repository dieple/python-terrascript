from awacs.aws import Action, Allow, PolicyDocument, Principal, Statement
from awacs.iam import ARN as IAM_ARN
import awacs.codebuild as codebuild
import awacs.codecommit as codecommit
import awacs.codedeploy as codedeploy
import awacs.iam as iam
import awacs.s3 as s3


# setup some dynamic required fields
def codepipeline_policy_document(input_kwargs, build_data):

  user = "root"
  account = build_data["account_id"]
  bucket_arn = "arn:aws:s3:::{0}".format(input_kwargs["name"])

  pd = PolicyDocument(
    Version="2012-10-17",
    Id="CodePipeline-Permissions",
    Statement=[
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          codebuild.StartBuild,
          codebuild.BatchGetBuilds,
          codedeploy.CreateDeployment,
          codedeploy.GetApplicationRevision,
          codedeploy.GetDeployment,
          codedeploy.GetDeploymentConfig,
          codedeploy.RegisterApplicationRevision,
          iam.PassRole,
          iam.GetRole,
          codecommit.GitPull
        ],
        Resource=['*']
      ),
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          s3.CreateBucket,
          s3.GetObject,
          s3.ListAccessPoints,
          s3.ListAllMyBuckets,
          s3.ListBucket,
          s3.ListBucketByTags,
          s3.ListBucketMultipartUploads,
          s3.ListBucketVersions,
          s3.ListJobs,
          s3.ListMultipartUploadParts,
          s3.ListObjects,
          s3.PutObject,
          s3.GetBucketAcl,
          s3.GetBucketLocation,
          s3.GetObjectVersion
        ],
        Resource=[bucket_arn]
      )
    ]
  )


  input_kwargs["policy"] = pd.to_json()

  return input_kwargs
