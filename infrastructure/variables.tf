variable "GOOGLE_CREDENTIALS" {
  type      = string
  sensitive = true
}

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

variable "firebase_app_name" {
  type    = string
  default = "RecipeDex"
}

variable "firestore_database_name" {
  type    = string
  default = "recipedex"
}

variable "firestore_database_type" {
  type    = string
  default = "FIRESTORE_NATIVE"
}

variable "artifact_registry_repository_name" {
  type    = string
  default = "recipedex"
}
