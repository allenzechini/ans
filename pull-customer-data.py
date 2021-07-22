import requests
import json
import os
from requests_oauthlib import OAuth2Session

# ID vars
# Client/JIRA info received from provider (Atlassian)
clientID = os.environ.get('PYAPP_CLIENTID')
clientSecret = os.environ.get('PYAPP_CLIENTSECRET')
workspaceID = os.environ.get('JIRA_WORKSPACEID')
ObjectIDs = {
  "ATOM": "22"
}

# URI vars
redirectURI = 'https://shotoverjira.atlassian.net'
authbaseURI = 'https://auth.atlassian.com/authorize'
accesstokenURI = 'https://auth.atlassian.com/oauth/token'
insightAPIURI = f'{redirectURI}/jsm/insight/workspace/{workspaceID}/v1/object/{ObjectIDs["ATOM"]}'
scopes = 'read:servicedesk-request read:servicemanagement-insight-objects'

# Create initial auth request
oauth = OAuth2Session(clientID, redirect_uri=redirectURI, scope=scopes)
authorization_url, state = oauth.authorization_url(authbaseURI)
print(f'Go to {authorization_url} to authorize access')
authorization_response = input('Enter the full callback URL: ')

# Fetch access token
token = oauth.fetch_token(
  accesstokenURI,
  authorization_response=authorization_response,
  client_secret=clientSecret
)

# Request data from resource
response = oauth.get(insightAPIURI)
response.json()

# Header var
#headers = {
#  "Accept": "application/json"
#}
#
#response = requests.request(
#  "GET",
#  url,
#  headers=headers
#)
#
#print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
#
#if __name__ == '__main__':
#  main()
