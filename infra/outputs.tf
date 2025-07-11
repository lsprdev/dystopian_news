output "database_uri" {
  value = digitalocean_database_cluster.postgres.uri
  sensitive = true
}