from awacs.aws import Action, Allow, PolicyDocument, Principal, Statement
from awacs.iam import ARN as IAM_ARN
import awacs.kms as kms


# setup some dynamic required fields
def kms_policy_document(input_kwargs, build_data):

  user = "root"
  account = build_data["account_id"]

  pd = PolicyDocument(
    Version="2012-10-17",
    Id="KMS-Account-Permissions",
    Statement=[
      Statement(
        Effect=Allow,
        Principal=Principal("AWS", [IAM_ARN(user, '', account)]),
        Action=[
          kms.CancelKeyDeletion,
          kms.ConnectCustomKeyStore,
          kms.CreateAlias,
          kms.CreateCustomKeyStore,
          kms.CreateGrant,
          kms.CreateKey,
          kms.Decrypt,
          kms.DeleteAlias,
          kms.DeleteCustomKeyStore,
          kms.DeleteImportedKeyMaterial,
          kms.DescribeCustomKeyStores,
          kms.DescribeKey,
          kms.DisableKey,
          kms.DisableKeyRotation,
          kms.DisconnectCustomKeyStore,
          kms.EnableKey,
          kms.EnableKeyRotation,
          kms.Encrypt,
          kms.GenerateDataKey,
          kms.GenerateDataKeyWithoutPlaintext,
          kms.GenerateRandom,
          kms.GetKeyPolicy,
          kms.GetKeyRotationStatus,
          kms.GetParametersForImport,
          kms.ImportKeyMaterial,
          kms.ListAliases,
          kms.ListGrants,
          kms.ListKeyPolicies,
          kms.ListKeys,
          kms.ListResourceTags,
          kms.ListRetirableGrants,
          kms.PutKeyPolicy,
          kms.ReEncrypt,
          kms.ReEncryptFrom,
          kms.ReEncryptTo,
          kms.RetireGrant,
          kms.RevokeGrant,
          kms.ScheduleKeyDeletion,
          kms.TagResource,
          kms.UntagResource,
          kms.UpdateAlias,
          kms.UpdateCustomKeyStore,
          kms.UpdateKeyDescription
        ],
        Resource=['*']
      )
    ]
  )


  input_kwargs["policy"] = pd.to_json()

  return input_kwargs
