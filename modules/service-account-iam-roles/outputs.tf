output "sa_iam_role_external_dns_arn" {
  value = module.external_dns_role.sa_iam_role_arn
}

output "sa_iam_role_cert_manager_arn" {
  value = module.cert_manager_role.sa_iam_role_arn
}

output "sa_iam_role_autoscaler_arn" {
  value = module.autoscaler_role.sa_iam_role_arn
}

output "sa_iam_role_vaultdb_arn" {
  value = module.vault_dynamodb_role.sa_iam_role_arn
}

output "sa_iam_role_alb_ing_controller_arn" {
  value = module.alb_ing_controller_role.sa_iam_role_arn
}
