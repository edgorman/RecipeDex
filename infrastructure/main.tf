terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.10.0"
    }
  }

  cloud {
    # can't be stored as secret
    organization = "recipedex"
    workspaces {
      tags = ["gcp"]
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_project_region
  zone    = var.gcp_project_zone
}

provider "google-beta" {
  project = var.gcp_project_id
  region  = var.gcp_project_region
  zone    = var.gcp_project_zone
}

resource "google_project_service" "cloudresourcemanager" {
  provider = google-beta
  project  = var.gcp_project_id
  service  = "cloudresourcemanager.googleapis.com"
}

resource "google_project_service" "serviceusage" {
  provider = google-beta
  project  = var.gcp_project_id
  service  = "serviceusage.googleapis.com"
}

resource "google_project_service" "firebase" {
  provider = google-beta
  service  = "firebase.googleapis.com"
  project  = var.gcp_project_id

  depends_on = [ 
    google_project_service.cloudresourcemanager,
    google_project_service.serviceusage
  ]
}

resource "google_firebase_project" "default" {
  provider = google-beta
  project  = var.gcp_project_id

  depends_on = [
    google_project_service.firebase,
  ]
}

resource "google_firebase_web_app" "default" {
  provider = google-beta
  project  = google_firebase_project.default.project

  display_name = var.firebase_app_name
}

# Note: enabling authentication in firebase must be done through firebase console
# see https://firebase.google.com/codelabs/firebase-terraform#5

resource "google_project_service" "vertexai" {
  provider = google-beta
  project  = var.gcp_project_id
  service  = "aiplatform.googleapis.com"

  depends_on = [
    google_project_service.cloudresourcemanager,
    google_project_service.serviceusage
  ]
}

resource "google_project_service" "run_api" {
  provider = google-beta
  project  = var.gcp_project_id
  service  = "run.googleapis.com"
}

resource "google_project_service" "artifactregistry" {
  provider = google-beta
  project  = var.gcp_project_id
  service  = "artifactregistry.googleapis.com"
}

resource "google_artifact_registry_repository" "recipedex_registry" {
  provider      = google-beta
  location      = var.gcp_project_region
  repository_id = var.artifact_registry_repository_name
  format        = "DOCKER"
  depends_on    = [
    google_project_service.artifactregistry
  ]
}
