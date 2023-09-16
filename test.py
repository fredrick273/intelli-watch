import requests
webhook_url = "https://discord.com/api/webhooks/1150122273722863688/WVy_o37CPBOZY6FQYNZ0g-s8MevY04LJGAp1lGnpDX5U8PP_6n8sCq0c2Rf_-28sBx_m"

while True:
    content = input('Enter msg:')
    message = {"content": content}
    requests.post(webhook_url, json=message)