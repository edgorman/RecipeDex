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

# TODO: Remove in subsequent PR
provider "google-beta" {
  project = var.gcp_project_id
  region  = var.gcp_project_region
  zone    = var.gcp_project_zone
}

resource "google_project_service" "firebase" {
  provider = google-beta
  service  = "firebase.googleapis.com"
  project  = var.gcp_project_id

  disable_on_destroy = true
  disable_dependent_services = true
}
