output "cluster_id" {
  value = module.eks.cluster_id
}

output "cluster_arn" {
  value = module.eks.cluster_arn
}

output "cluster_certificate_authority_data" {
  value = module.eks.cluster_certificate_authority_data
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "cluster_version" {
  value = module.eks.cluster_version
}

output "cluster_security_group_id" {
  value = module.eks.cluster_security_group_id
}

output "config_map_aws_auth" {
  value = module.eks.config_map_aws_auth
}

output "cluster_iam_role_name" {
  value = module.eks.cluster_iam_role_name
}

output "cluster_iam_role_arn" {
  value = module.eks.cluster_iam_role_arn
}

output "kubeconfig" {
  value = module.eks.kubeconfig
}

output "kubeconfig_filename" {
  value = module.eks.kubeconfig_filename
}

output "workers_asg_names" {
  value = module.eks.workers_asg_names
}

output "workers_default_ami_id" {
  value = module.eks.workers_default_ami_id
}

output "worker_security_group_id" {
  value = module.eks.worker_security_group_id
}

output "worker_iam_instance_profile_arns" {
  value = module.eks.worker_iam_instance_profile_arns
}

output "worker_iam_role_name" {
  value = module.eks.worker_iam_role_name
}

output "worker_iam_role_arn" {
  value = module.eks.worker_iam_role_arn
}

output "node_groups" {
  value = module.eks.node_groups
}

output "workers_asg_arns" {
  value = module.eks.workers_asg_arns
}

output "worker_iam_instance_profile_names" {
  value = module.eks.worker_iam_instance_profile_names
}

output "workers_launch_template_arns" {
  value = module.eks.workers_launch_template_arns
}

output "workers_launch_template_ids" {
  value = module.eks.workers_launch_template_ids
}

output "workers_launch_template_latest_versions" {
  value = module.eks.workers_launch_template_latest_versions
}

output "workers_user_data" {
  value = module.eks.workers_user_data
}

