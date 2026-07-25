terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "lab" {
  name     = "devsecops-rg"
  location = "East US"
}

resource "azurerm_storage_account" "lab_storage" {
  name                     = "devsecopsstorageacct"
  resource_group_name      = azurerm_resource_group.lab.name
  location                 = azurerm_resource_group.lab.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  # DELIBERATE VULNERABILITY: Allowing HTTP traffic instead of strictly HTTPS
  enable_https_traffic_only = false
}