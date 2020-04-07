from awacs.aws import Action, Allow, PolicyDocument, Principal, Statement
from awacs.iam import ARN as IAM_ARN
import awacs.codebuild as codebuild
import awacs.codecommit as codecommit
import awacs.iam as iam
import awacs.logs as logs
import awacs.s3 as s3
import awacs.ecr as ecr
import awacs.ec2 as ec2
import awacs.ecs as ecs


# setup some dynamic required fields
def codebuild_policy_document(input_kwargs, build_data):

  user = "root"
  account = build_data["account_id"]

  pd = PolicyDocument(
    Version="2012-10-17",
    Id="Codebuild-Permissions",
    Statement=[
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          codebuild.BatchDeleteBuilds,
          codebuild.BatchGetBuilds,
          codebuild.BatchGetProjects,
          codebuild.BatchGetReportGroups,
          codebuild.BatchGetReports,
          codebuild.BatchPutTestCases,
          codebuild.CreateProject,
          codebuild.CreateReport,
          codebuild.CreateReportGroup,
          codebuild.CreateWebhook,
          codebuild.DeleteOAuthToken,
          codebuild.DeleteProject,
          codebuild.DeleteReport,
          codebuild.DeleteReportGroup,
          codebuild.DeleteResourcePolicy,
          codebuild.DeleteSourceCredentials,
          codebuild.DeleteWebhook,
          codebuild.DescribeTestCases,
          codebuild.GetResourcePolicy,
          codebuild.ImportSourceCredentials,
          codebuild.InvalidateProjectCache,
          codebuild.ListBuilds,
          codebuild.ListBuildsForProject,
          codebuild.ListConnectedOAuthAccounts,
          codebuild.ListCuratedEnvironmentImages,
          codebuild.ListProjects,
          codebuild.ListReportGroups,
          codebuild.ListReports,
          codebuild.ListReportsForReportGroup,
          codebuild.ListRepositories,
          codebuild.ListSharedProjects,
          codebuild.ListSharedReportGroups,
          codebuild.ListSourceCredentials,
          codebuild.PersistOAuthToken,
          codebuild.PutResourcePolicy,
          codebuild.StartBuild,
          codebuild.StopBuild,
          codebuild.UpdateProject,
          codebuild.UpdateReport,
          codebuild.UpdateReportGroup,
          codebuild.UpdateWebhook,
          iam.PassRole,
          codecommit.GitPull
        ],
        Resource=['*']
      ),
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          logs.FilterLogEventlogs,
          logs.GetLogEvents,
          logs.CreateLogGroup,
          logs.CreateLogStream,
          logs.PutLogEvents
        ],
        Resource=['*']
      ),
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          s3.CreateBucket,
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
          s3.GetObject,
          s3.GetBucketAcl,
          s3.GetBucketLocation,
          s3.GetObjectVersion
        ],
        Resource=['*']
      ),
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          ecr.BatchCheckLayerAvailability,
          ecr.GetDownloadUrlForLayer,
          ecr.BatchGetImage,
          ecr.PutImage,
          ecr.InitiateLayerUpload,
          ecr.UploadLayerPart,
          ecr.CompleteLayerUpload,
          ecr.GetAuthorizationToken
          ],
        Resource=['*']
      ),
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          ec2.DescribeSecurityGroups,
          ec2.DescribeSubnets
        ],
        Resource=['*']
      ),
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          ecs.RegisterTaskDefinition,
          ecs.DescribeTaskDefinition,
          ecs.DescribeServices,
          ecs.CreateService,
          ecs.ListServices,
          ecs.UpdateService
        ],
        Resource=['*']
      ),
    ]
  )


  input_kwargs["policy"] = pd.to_json()

  return input_kwargs
