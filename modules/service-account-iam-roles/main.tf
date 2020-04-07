data "terraform_remote_state" "eks" {
  backend = "s3"
  config = {
    bucket         = var.bucket
    key            = format("env:/%s/%s/%s", var.workspace, "eks", "terraform.tfstate")
    region         = var.bucket_region
    dynamodb_table = var.dynamodb
  }
}

data "terraform_remote_state" "dynamodb" {
  backend = "s3"
  config = {
    bucket         = var.bucket
    key            = format("env:/%s/%s/%s", var.workspace, "dynamodb", "terraform.tfstate")
    region         = var.bucket_region
    dynamodb_table = var.dynamodb
  }
}

data "aws_eks_cluster" "cluster" {
  name = data.terraform_remote_state.eks.outputs.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = data.terraform_remote_state.eks.outputs.cluster_id
}

module "external_dns_role" {
  source = "git::https://github.com/dieple/terraform-framework.git//modules/iam-users-and-accounts/eks-sa-iam-role?ref=tags/v0.0.7"

  enabled            = var.create_ext_dns_role
  name               = var.ext_dns_role
  cluster_name       = data.aws_eks_cluster.cluster.name
  oidc_provider      = data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer
  sa_ns              = var.ext_dns_ns
  sa_iam_policy_json = data.aws_iam_policy_document.ext_dns.json
  tags               = var.tags
}

module "cert_manager_role" {
  source = "git::https://github.com/dieple/terraform-framework.git//modules/iam-users-and-accounts/eks-sa-iam-role?ref=tags/v0.0.7"

  enabled            = var.create_cert_manager_role
  name               = var.cert_manager_role
  cluster_name       = data.aws_eks_cluster.cluster.name
  oidc_provider      = data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer
  sa_ns              = var.cert_manager_ns
  sa_iam_policy_json = data.aws_iam_policy_document.letsencrypt.json
  tags               = var.tags
}

module "autoscaler_role" {
  source = "git::https://github.com/dieple/terraform-framework.git//modules/iam-users-and-accounts/eks-sa-iam-role?ref=tags/v0.0.7"

  enabled            = var.create_autoscaler_role
  name               = var.autoscaler_role
  cluster_name       = data.aws_eks_cluster.cluster.name
  oidc_provider      = data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer
  sa_ns              = var.autoscaler_ns
  sa_iam_policy_json = data.aws_iam_policy_document.autoscaler.json
  tags               = var.tags
}

module "vault_dynamodb_role" {
  source = "git::https://github.com/dieple/terraform-framework.git//modules/iam-users-and-accounts/eks-sa-iam-role?ref=tags/v0.0.7"

  enabled            = var.create_vault_dynamodb_role
  name               = var.vault_dynamodb_role
  cluster_name       = data.aws_eks_cluster.cluster.name
  oidc_provider      = data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer
  sa_ns              = var.vault_dynamodb_ns
  sa_iam_policy_json = data.aws_iam_policy_document.vault_dynamodb.json
  tags               = var.tags
}

module "alb_ing_controller_role" {
  source = "git::https://github.com/dieple/terraform-framework.git//modules/iam-users-and-accounts/eks-sa-iam-role?ref=tags/v0.0.7"

  enabled            = var.create_alb_ing_controller_role
  name               = var.alb_ing_controller_role
  cluster_name       = data.aws_eks_cluster.cluster.name
  oidc_provider      = data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer
  sa_ns              = var.alb_ing_controller_ns
  sa_iam_policy_json = data.aws_iam_policy_document.alb_ing_controller.json
  tags               = var.tags
}

//module "vault_iam_role" {
//  source = "../../../modules/iam-users-and-accounts/iam-role"
//
//  enabled            = var.create_vault_iam_role
//  name               = format("%s-%s", module.tag_label.id, "vault")
//  policy_description = "Allow Vault to Access Dynamodb"
//  role_description   = "IAM role with permissions to perform actions on dynamodb resources"
//  policy_documents   = [data.aws_iam_policy_document.vault_dynamodb.json]
//
//  principals = {
//    Service = ["ec2.amazonaws.com", "eks.amazonaws.com"]
//  }
//
//  tags = module.tag_label.tags
//}
