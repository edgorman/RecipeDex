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

variable "firestore_collection_recipe_name" {
  type    = string
  default = "recipe"
}

variable "firestore_collection_user_name" {
  type    = string
  default = "user"
}

variable "firestore_collection_session_name" {
  type    = string
  default = "session"
}

variable "artifact_registry_repository_name" {
  type    = string
  default = "recipedex"
}
