import requests
import json
import os
#from requests_oauthlib import OAuth2Session

# ID vars
# Client/JIRA info received from provider (Atlassian)
#clientID = os.environ.get('PYAPP_CLIENTID')
#clientSecret = os.environ.get('PYAPP_CLIENTSECRET')
basic_auth  = os.environ.get('JIRA_BASICAUTH')
workspaceID = os.environ.get('JIRA_WORKSPACEID')
ObjectIDs   = {
  "ATOM": "22"
}

# URI vars
#redirectURI = 'https://shotoverjira.atlassian.net'
#authbaseURI = 'https://auth.atlassian.com/authorize'
#accesstokenURI = 'https://auth.atlassian.com/oauth/token'
#insightAPIURI = f'{redirectURI}/jsm/insight/workspace/{workspaceID}/v1/object/{ObjectIDs["ATOM"]}'
#scopes = 'read:servicedesk-request read:servicemanagement-insight-objects'

# Create initial auth request
#oauth = OAuth2Session(clientID, redirect_uri=redirectURI, scope=scopes)
#authorization_url, state = oauth.authorization_url(authbaseURI)
#print(f'Go to {authorization_url} to authorize access')
#authorization_response = input('Enter the full callback URL: ')
#
## Fetch access token
#token = oauth.fetch_token(
#  accesstokenURI,
#  authorization_response=authorization_response,
#  client_secret=clientSecret
#)
#
## Request data from resource
#response = oauth.get(insightAPIURI)
#response.json()

# This code sample uses the 'requests' library:
# http://docs.python-requests.org
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
