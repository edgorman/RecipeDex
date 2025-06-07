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

variable "GOOGLE_CREDENTIALS" {
  type      = string
  sensitive = true
}

variable "firebase_app_name" {
  type    = string
  default = "RecipeDex"
}

variable "backend_service_name" {
  type    = string
  default = "backend"
}
