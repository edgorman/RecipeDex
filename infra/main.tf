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
  credentials = var.gcp_terraform_cloud_service_account_credentials
}
