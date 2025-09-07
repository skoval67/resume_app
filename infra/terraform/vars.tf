variable "YC_KEYS" {
  type = object({
    folder_id          = string
    service_account_id = string
  })
  description = "ID облака YC и сервисного аккаунта"
}

variable "image_debian_id" {
  type        = string
  description = "debian 12"
  default     = "fd83pnjq4iagnphjuhr5"
}

variable "site_name" {
  type        = string
  description = "DNS-имя сайта"
}
