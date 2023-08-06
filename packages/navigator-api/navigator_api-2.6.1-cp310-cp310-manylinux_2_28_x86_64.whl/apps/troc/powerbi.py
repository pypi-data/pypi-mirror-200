import asyncio
import uuid
import urllib3
urllib3.disable_warnings()
from functools import partial
from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor
import requests
import aiohttp
from aiohttp import web
from bs4 import BeautifulSoup as bs
from navigator.conf import config
import msal
import logging

proxy = {
    "http" :"127.0.0.1:8800"
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2810.1 Safari/537.36',
    'Accept': 'text/html',
    'Content-Type': 'text/html'
}

TENANT = 'af176793-abc4-423e-8fab-dfc4e2bf8b9d'
CLIENT_ID = "a9d1de54-c22b-45e7-bf3f-1c621b38bcb8"
CLIENT_SECRET = "p-aPPVYu2HQ6JpxH~580z5Um-s419v.6t3"
cache = msal.SerializableTokenCache()
SCOPE = ["User.ReadBasic.All"]

# Authorize URL
authorize_url = 'https://login.microsoftonline.com/{}'.format(TENANT)

def build_msal_app(client):
    app = msal.PublicClientApplication(
        client,
        authority=authorize_url,
        token_cache=cache
    )
    return app
    # return msal.ConfidentialClientApplication(
    #         CLIENT_ID, authority=authorize_url,
    #         client_credential=CLIENT_SECRET, token_cache=cache)


app = build_msal_app(CLIENT_ID)
print(app)

async def connect(url, auth):
    loop = asyncio.get_event_loop()
    s = requests.Session()
    user = config.get('EMAIL_O365')
    pwd = config.get('PWD_O365')

    account = app.get_accounts(username=user)
    print(account)
    result = None
    if account:
        logging.info("Account(s) exists in cache, probably with token too. Let's try.")
        result = app.acquire_token_silent(SCOPE, account=account[0])

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        # See this page for constraints of Username Password Flow.
        # https://github.com/AzureAD/microsoft-authentication-library-for-python/wiki/Username-Password-Authentication
        result = app.acquire_token_by_username_password(user, pwd, scopes=SCOPE)
    print(result)
    # payload = {
    #         'client_id': CLIENT_ID, # Variable exists but not exposed in this question
    #         'response_type': 'code',
    #         'redirect_uri': url,
    #         'resource': 'https://analysis.windows.net/powerbi/api',
    #         'response_mode': 'form_post',
    #         'domain_hint': 'trocglobal.com',
    #         'domain': 'trocglobal.com',
    #         'grant_type':'password',
    #         #'scope':'openid',
    #         "scope": ["https://graph.microsoft.com/.default"],
    #         'username': user,
    #         'password': pwd,
    #         #'site_id': 500453
    # }
    #
    if result:
        executor = ThreadPoolExecutor(2) # running in a thread Pool Executor
        headers['Authorization'] = 'Bearer {}'.format(result['access_token'])
        my_request = partial(s.get, headers=headers, auth=auth, proxies=proxy)
        future = [
            loop.run_in_executor(executor, my_request, url)
        ]
        resp = ''
        for response in await asyncio.gather(*future):
            print(response)
            #if response.status_code == 200:
            #    #resp = bs(response.text, 'html.parser')
            resp = response.text
        return resp
    else:
        return None

async def powerbi(request):
    auth=HTTPBasicAuth(config.get('EMAIL_O365'), config.get('PWD_O365'))
    #url = 'https://app.powerbi.com/groups/me/reports/40d32681-2a30-4289-a8da-adaa43661d08/ReportSectionc958280305d6941b0630?route=sharedwithme%2Freports%2F40d32681-2a30-4289-a8da-adaa43661d08%2FReportSectionc958280305d6941b0630&noSignUpCheck=1'
    #url = 'https://app.powerbi.com/'
    #url = 'https://graph.microsoft.com/v1.0/users'
    url = 'https://symbits-my.sharepoint.com/personal/jlara_trocglobal_com/_layouts/15/onedrive.aspx'
    response = await connect(url, auth)
    #response = '<h1>Hello World</h1>'
    return web.Response(body=response, content_type='text/html', status=200)
