import os
import json
import requests

# ID vars
basic_auth  = os.environ.get('JIRA_BASICAUTH')
workspaceID = os.environ.get('JIRA_WORKSPACEID')

#ObjectIDs   = {
#  "ATOM": "22"
#}

# Instead of using dictionaries, thinking of using tuples, like this...
# ATOM = ("ATOM", 22, 308, 312)
# Where:
#   "ATOM" = name of product
#   22     = product_id
#   308    = name_id
#   312    = org_id

url = "https://api.atlassian.com/jsm/insight/workspace/{workspaceId}/v{version}/object/navlist/iql"
headers = {
  "Accept": "application/json",
  "Authorization": "Basic " + basic_auth,
  "Content-Type": "application/json"
}

def get_products(product="ATOM", product_id="22", name_id="308", org_id="312"):
  payload = json.dumps({
    "iql": "objectType = " + product,
    "objectTypeId": product_id,
    "page": 1,
    "resultsPerPage": 600,
    "includeAttributes": true,
    "attributesToDisplay": {
      "attributesToDisplayIds": [
        name_id,
        ord_id
      ]
    },
    "objectSchemaId": "4"
  })

  response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers
  )

  print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

#def main():
#  call API
#  print to file
#
#if __name__ == '__main__':
#  main()
