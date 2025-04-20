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
  project     = var.gcp_project_id
  region      = var.gcp_project_region
  zone        = var.gcp_project_zone
}

provider "google-beta" {
  project     = var.gcp_project_id
  region      = var.gcp_project_region
  zone        = var.gcp_project_zone
}

resource "google_project_service" "firebase" {
  service = "firebase.googleapis.com"
  project = var.gcp_project_id
}

resource "google_firebase_project" "default" {
  provider = google-beta
  project = var.gcp_project_id
}
