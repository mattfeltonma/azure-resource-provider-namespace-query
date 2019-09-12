# Azure Resource Provider Namespace Query
This Python solution queries the Azure REST API for the listing of aliases for an Azure resource provider namespace

## What problem does this solve?
Creating new policies for use with Azure Policy requires the usage of resource provider namespace aliases.  These aliases map to specific resource properties.  This solution produces a CSV containing all of the aliases and relevant resource properties for a given namespace.  Retrieving a current listing of aliases requires a query to the Azure REST API or the usage of Azure CLI or PowerShell, 

This Python solution can be used to query a resource provider namespace for all of the aliases and the resource properties they map to.

## Requirements

### Python Runtime and Modules
* [Python 3.6](https://www.python.org/downloads/release/python-360/)
* [MSAL](https://github.com/AzureAD/microsoft-authentication-library-for-python)

## Azure Requirements
* [Application Registered with Azure AD as Confidential Client](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal)
* Service principal must be granted Reader on Azure subscription

## Setup

Ensure the appropriate Python modules are installed.

python azure_policy_evaluate.py --tenantname TENANTNAME --clientid CLIENTID --clientsecret CLIENTSECRET --subscriptionid SUB_ID [--logfile]

python policy.py --tenantname TENANT_NAME --subscriptionid SUBSCRIPTION_ID --clientid CLIENT_ID --clientsecret CLIENT_SECRET --resourceprovider RESOURCE_PROVIDER_NAMESPACE --exportfile FULL_PATH_TO_EXPORT_FILE
