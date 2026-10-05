terraform {
  required_providers {
    minikube = {
      source  = "scott-the-programmer/minikube"
      version = "0.8.0"
    }
  }
}

provider "minikube" {
  kubernetes_version = "v1.37.0"
}

resource "minikube_cluster" "minikube_docker" {
  driver       = "docker"
  cluster_name = "devopsrun"
  addons = [
    "default-storageclass", "storage-provisioner"
  ]
}
