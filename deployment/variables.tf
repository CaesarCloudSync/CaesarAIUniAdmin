variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "caesaraiapis"
}

variable "region" {
  description = "GCP region for Cloud Run"
  type        = string
  default     = "us-central1"
}

variable "image" {
  description = "Docker image for Cloud Run"
  type        = string
}

variable "service_name" {
  description = "Name of the Cloud Run service"
  type        = string
}
variable "google_gemini_api_key" {
  description = "Path to the GCP service account key file"
  type        = string
  default     = "service_account.json"
}

variable "secret_id" {
  description = "Secret ID for the service account key in Secret Manager"
  type        = string
}

