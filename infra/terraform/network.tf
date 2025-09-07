locals {
  ingresses = [
    { port : "22", cidr : ["0.0.0.0/0"] },
    { port : "443", cidr : ["0.0.0.0/0"] },
    { port : "80", cidr : ["0.0.0.0/0"] }
  ]
}

resource "yandex_vpc_network" "network1" {
  name = "network1"
}

resource "yandex_vpc_subnet" "subnet-1" {
  name           = "subnet1"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network1.id
  v4_cidr_blocks = ["192.168.10.0/24"]
  route_table_id = yandex_vpc_route_table.rt.id
}

resource "yandex_vpc_gateway" "nat_gateway" {
  name = "nat-gateway"
  shared_egress_gateway {}
}

resource "yandex_vpc_route_table" "rt" {
  name       = "route-to-internet"
  network_id = yandex_vpc_network.network1.id

  static_route {
    destination_prefix = "0.0.0.0/0"
    gateway_id         = yandex_vpc_gateway.nat_gateway.id
  }
}

resource "yandex_vpc_security_group" "sg-srvr" {
  name       = "sg-srvr"
  network_id = yandex_vpc_network.network1.id

  egress {
    protocol       = "ANY"
    description    = "any"
    v4_cidr_blocks = ["0.0.0.0/0"]
    from_port      = 1
    to_port        = 65535
  }

  dynamic "ingress" {
    for_each = local.ingresses
    content {
      protocol       = "TCP"
      v4_cidr_blocks = ingress.value["cidr"]
      port           = ingress.value["port"]
    }
  }
}
