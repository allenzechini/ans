import os
import json
import requests

# URL vars
basic_auth  = os.environ.get('JIRA_BASICAUTH')
workspaceID = os.environ.get('JIRA_WORKSPACEID')
version     = "1"

# Products & IDs
ProductIDs = {
  "ATOM": (22, 308, 312),
  "ION": (12, 86, 90),
  "ARS-600": (35, 423, 427),
  "ARS-500": (8, 37, 51),
  "ARS-400": (14, 108, 112),
  "ARS-Redbox": (34, 404, 408),
  "ARS-KB-R": (16, 130, 134),
  "ARS-KB-H": (17, 141, 145),
  "GETAC-F110": (28, 359, 480),
  "PAN-GCS": (29, 363, 479),
  "NUC-GCS": (30, 367, 478),
  "RP-1": (31, 375, 379),
  "MC1-CPU-25": (32, 387, 391),
  "EARTH-QUARK": (33, 399, 477)
}

url = f"https://api.atlassian.com/jsm/insight/workspace/{workspaceID}/v{version}/object/navlist/iql"
headers = {
  "Accept": "application/json",
  "Authorization": f"Basic {basic_auth}",
  "Content-Type": "application/json"
}

def get_product(fh, product_name, product_id, name_id, org_id):
  payload = json.dumps({
    "iql": f"objectType = {product_name}",
    "objectTypeId": product_id,
    "page": 1,
    "resultsPerPage": 600,
    "includeAttributes": "true",
    "attributesToDisplay": {
      "attributesToDisplayIds": [
        name_id,
        org_id
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

  # Parse response
  r_json = response.json()
  for i in range(len(r_json["objectEntries"])):
    name   = r_json["objectEntries"][i]["attributes"][0]["objectAttributeValues"][0]["displayValue"]
    org    = r_json["objectEntries"][i]["attributes"][1]["objectAttributeValues"][0]["displayValue"]
    prod   = name.split()[0]
    serial = name.split()[2]
    data   = f"{prod}|{serial}|{org}"
    fh.write(f"{data}\n")

def main():
  with open('product_info.txt.python', 'w') as f:
    for key in ProductIDs:
      # Use dict key as product_name, dict values for rest of the args
      get_product(f, key, *ProductIDs[key])
  
if __name__ == '__main__':
  main()
