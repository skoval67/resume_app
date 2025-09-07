# разворачиваем окружение в YC
terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  # zone      = "ru-central1-a"
  folder_id = var.YC_KEYS.folder_id
}
