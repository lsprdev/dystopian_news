resource "digitalocean_kubernetes_cluster" "main" {
  name    = "k8s-cluster"
  region  = "nyc1"
  version = "latest"

  node_pool {
    name       = "default-pool"
    size       = "s-2vcpu-4gb"
    node_count = 3
  }
}