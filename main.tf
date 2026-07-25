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

  # FIX 1: Enforce HTTPS only (Resolves CKV_AZURE_3)
  enable_https_traffic_only = true

  # FIX 2: Enforce modern encryption (Resolves CKV_AZURE_44)
  min_tls_version           = "TLS1_2"

  # FIX 3: Block anonymous public access (Resolves CKV_AZURE_59 & CKV_AZURE_190)
  public_network_access_enabled = false

  # Ignore the replication warning for this specific lab environment
  # checkov:skip=CKV_AZURE_206: LRS is sufficient for this non-production lab.
}