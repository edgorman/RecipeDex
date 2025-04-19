variable "gcp_project_id" {
  type      = string
  sensitive = true
}

variable "gcp_project_region" {
  type      = string
  sensitive = true
}

variable "gcp_project_zone" {
  type      = string
  sensitive = true
}

variable "gcp_terraform_service_account_credentials" {
  type      = string
  sensitive = true
}
