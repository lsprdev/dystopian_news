terraform {
  backend "remote" {
    organization = "lsprsystems"

    workspaces {
      name = "dystopian_news"
    }
  }

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

variable "do_token" {}

provider "digitalocean" {
  token = var.do_token
}
