from urllib.parse import urlencode

# use https://vk.com/dev/
oauth_api_base_url = 'https://oauth.vk.com/authorize'
APP_ID = 7649081
redirect_uri = 'https://oauth.vk.com/blank.html'
scope = 'friends'

oauth_params = {
    'redirect_uri': redirect_uri,
    'scope': scope,
    'response_type': 'token',
    'client_id': APP_ID
}

print('?'.join([oauth_api_base_url, urlencode(oauth_params)]))
# follow the link you received and select in it TOKEN
