terraform {
  required_version = ">= 0.14"

  required_providers {
    # Cloud Run support was added on 3.3.0
    google = ">= 3.3"
  }
}

provider "google" {
  # Replace `PROJECT_ID` with your project
  project = "caesaraiapis"
}

# Enables the Cloud Run API
resource "google_project_service" "run_api" {
  service = "run.googleapis.com"
  disable_on_destroy = true
}

# Data source for the existing secret
data "google_secret_manager_secret" "amari_dev_api_key_secret" {
  secret_id = "amari-dev-gemini-api-key"
}

# Grant the Cloud Run service account permission to access the secret
resource "google_secret_manager_secret_iam_member" "secret_access" {
  secret_id = data.google_secret_manager_secret.amari_dev_api_key_secret.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:amari-dev-secret-accessor@caesaraiapis.iam.gserviceaccount.com"
}

# Cloud Run v2 service resource
resource "google_cloud_run_v2_service" "run_service" {
  name     = "caesaraiaptemotj"
  location = "us-central1"
  deletion_protection = false 
  template {
    containers {
      image = "palondomus/caesaraiaptemotj:16"
      env {
        name = "GOOGLE_GEMINI_API_KEY"
        value_source {
          secret_key_ref {
            # Fix: Reference the data source here
            secret  = data.google_secret_manager_secret.amari_dev_api_key_secret.secret_id
            version = "latest"
          }
        }
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [google_project_service.run_api]
}

# Allow unauthenticated users to invoke the service
resource "google_cloud_run_v2_service_iam_member" "noauth" {
  location = google_cloud_run_v2_service.run_service.location
  name     = google_cloud_run_v2_service.run_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Display the service URL
output "service_url" {
  value = google_cloud_run_v2_service.run_service.uri
}