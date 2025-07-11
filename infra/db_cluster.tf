resource "digitalocean_database_cluster" "postgres" {
  name       = "lsprdb"
  engine     = "pg"
  version    = "15"
  size       = "db-s-1vcpu-1gb"
  region     = "nyc1"
  node_count = 1
}