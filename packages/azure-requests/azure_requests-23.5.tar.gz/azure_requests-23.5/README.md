# Azure requests

Just a wrapper around Python requests module for communicating with Azure DevOps.

## DRY (don't repeat yourself) features

- Authentication
- Replace organization, project, and team in URL, so URLs can be copy-pasted from the documentation
- Handle rate limit
- Handle ADO temporary server errors
- Set appropriate Content-Type headers
- Parse JSON automatically
- Raise exception for wrong HTTPS statuses

## Rationale

Azure DevOps has an excellent HTTPS API with an excellent documentation. It is easy to understand and easy to use. For smaller scripts and projects it is easier to use them as is. Every existing API implementations have many documentation issues.

## Example

```python
from azure_requests import AzureRequests

azure_requests = AzureRequests(
    pat="<YOUR PAT>",
    organization="<YOUR ORGANIZATION>",
)

work_item = azure_requests.api(
    # Copy-pasted from https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/get-work-item?view=azure-devops-rest-7.0&tabs=HTTP
    "GET https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0",
    # custom URL parameters
    id=12345,
).request()

print(work_item)
```

For a more detailed example see `example.py`.
