# -----------------------------------
# Outputs
# -----------------------------------
output "google_gemini_sa_email" {
  value = google_service_account.google_gemini_sa.email
}

output "secret_id" {
  value = google_secret_manager_secret.service_account_key.secret_id
}
