#reddit api info

import requests
import requests.auth
import os
import pandas as pd
# authorize.py
import random


# def get_refresh_token():
#     url = requests.client.auth.url(duration='permanent', scopes=['read'], state=str(random.randint(0, 65000)))
#     print("Open this url in your browser to get refresh token: {url}".format(url=url))
#     params = self._get_params()
#     refresh_token = self.client.auth.authorize(params["code"])
#     return refresh_token

def get_token():

    client_id = '-57PYw9h0sLCjt5cUBbDlg'
    secret = '-tGOb2ej_ohxCNQGTKRiDbtIEayosw'
    auth = requests.auth.HTTPBasicAuth(client_id, secret)

    with open('pw.txt', 'r') as f:
        pw = f.read()

    data = {
        "grant_type": "password",
        #'grant_type': 'password',
        'username': ' nlp42069',
        'password': pw
    }

    headers = {'User-Agent': 'MyAPI/0.0.1'}

    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth,
                        data=data, headers=headers)
    print(res.json())
    if res != 200:
        return False

    token = res.json()['access_token']
    headers['Authorization'] = f'bearer  {token}'
    #headers = {**headers, **{'Authorization': f'bearer {token}'}}
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).json()

    res = requests.get('https://oauth.reddit.com/r/UCSC/hot',
                     headers=headers)

    df = pd.DataFrame()
    keys = 0

    for post in res.json()['data']['children']:
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'score': post['data']['score'],
            #'kind': post['kind'],

            #'ups': post['data']['ups'],
            #'downs': post['data']['downs'],
            }, ignore_index=True) #most popular reddit post title

        keys = post['data'].keys()

    print(keys)

    df.to_csv('ucsc_hottest_reddit_post.csv')
    f.close()

    #GET /api/v1/subreddit/emojis/all

    #most recent posts
    res = requests.get('https://oauth.reddit.com/r/UCSC/new',
                     headers=headers, params={'limit': '100'})

    df = pd.DataFrame()

    for post in res.json()['data']['children']:
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'score': post['data']['score']
            # 'ups': post['data']['ups'],
            # 'downs': post['data']['downs'],
        }, ignore_index=True)  # most popular reddit post title

        keys = post['data'].keys()
    print(keys)

    df.to_csv('ucsc_newest_reddit_post.csv')
    f.close()


if __name__ == '__main__':

    get_token()