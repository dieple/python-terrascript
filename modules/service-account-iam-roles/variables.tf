variable "ext_dns_ns" {
  type        = string
  default     = "external-dns"
}

variable "ext_dns_role" {
  description = "IRSA name suffix for external DNS EKS service"
  type        = string
  default     = "external-dns"
}

variable "create_ext_dns_role" {
  type        = bool
  default     = false
}

variable "hosted_zone_id" {
  description = "DNS zone ID that is with EKS external DNS service"
  type        = string
  default     = ""
}
variable "cert_manager_role" {
  description = "IRSA name suffix for cert_manager EKS service"
  type        = string
  default     = "cert-manager"
}
variable "cert_manager_ns" {
  type        = string
  default     = "cert-manager"
}
variable "create_cert_manager_role" {
  type        = bool
  default     = false
}

variable "autoscaler_role" {
  description = "IRSA name suffix for autoscaler EKS service"
  type        = string
  default     = "autoscaler"
}

variable "autoscaler_ns" {
  type        = string
  default     = "autoscaler"
}

variable "create_autoscaler_role" {
  type        = bool
  default     = false
}

variable "vault_dynamodb_role" {
  description = "IRSA name suffix for vault EKS service to access DynamoDB"
  type        = string
  default     = "vault"
}

variable "vault_dynamodb_ns" {
  type        = string
  default     = "vault"
}

variable "create_vault_dynamodb_role" {
  type        = bool
  default     = false
}

variable "alb_ing_controller_role" {
  description = "IRSA name suffix for ALB Ingress Controller on EKS"
  type        = string
  default     = "alb-ing-controller"
}

variable "alb_ing_controller_ns" {
  type        = string
  default     = "alb-ing-controller"
}

variable "create_alb_ing_controller_role" {
  type        = bool
  default     = false
}

variable "create_vault_iam_role" {
  type        = bool
  default     = false
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "bucket" {
  type = string
}

variable "bucket_region" {
  type = string
}

variable "dynamodb" {
  type = string
}

variable "workspace" {
  type = string
}