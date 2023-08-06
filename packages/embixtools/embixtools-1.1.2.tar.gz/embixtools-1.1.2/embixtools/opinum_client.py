import requests
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
from functools import wraps
from datetime import datetime as dt, timedelta as td
import logging
import pandas as pd

iso = "%Y-%m-%dT%H:%M:%S"

class Opinum(object):
    
    def __init__(self, usr, pwd, client_id, client_secret):
        self.username = usr
        self.password = pwd
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = ''
        self.token_expiration = dt(1000,1,1)

    @property
    def sites(self):
        return self.request('GET','sites').json()

    @property
    def sources(self):
        return self.request('GET','sources', params = {'sourcesFilter.displayLevel': 'Site'}).json()

    @property
    def variables(self):
        return self.request('GET','variables').json()

    @property
    def timeseries(self):
        sources = self.sources
        variables = self.variables
        return [
            {
                'id': variable['id'],
                'site': source['siteName'],
                'source': source['name'],
                'name': variable['name'],
            }
            for source in sources
            for variable in variables if variable['sourceId'] == source['id']
        ]

    def auth(self):
        oauth = OAuth2Session(
            client = LegacyApplicationClient(client_id=self.client_id)
        )
        token = oauth.fetch_token(
            token_url = 'https://identity.opinum.com/connect/token',
            scope = 'opisense-api push-data',
            username = self.username,
            password = self.password,
            client_id = self.client_id,
            client_secret = self.client_secret,
            auth = None
        )
        self.token =  'Bearer ' + token['access_token']
        self.token_expiration = dt.utcnow() + td(seconds=60)
        oauth.close()
        return self.token
    
    def var(self, site, source, variable):
        try:
            return [
                ts['id'] for ts in self.timeseries 
                if all((ts['site'] == site, ts['source'] == source, ts['name'] == variable))
            ][0]
        except:
            return -1

    def token_required(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if dt.utcnow() > self.token_expiration:
                self.auth()
            return func(self, *args, **kwargs)
        return wrapper
    
    @token_required
    def request(self, method, url, data={}, params={}, headers={}):
        return requests.request(
            method = method,
            url = f'https://api.opinum.com/{url}',
            params = params,
            headers = {**headers, 'Authorization': self.token},
            json = data
        )

    @token_required
    def push(self, dps):
        resp = requests.post(
            url = 'https://push.opinum.com/api/data',
            json = dps,
            headers = {
                'Authorization': self.token,
            },
            # mode = "cors"
        )
        return resp
    
    @token_required
    def get_dps(self, site, source, variable, interval=None):
        params = {
            'filter.variableId': self.var(site, source, variable),
            'filter.displayLevel': 'ValueVariableDate',
            'filter.includeToBoundary': True
        }
        if not interval is None:
            params['filter.from'] = interval[0].strftime(iso)
            params['filter.to'] = interval[1].strftime(iso)
        try:
            data = self.request(method='GET', url='data', params=params).json()
            return [{'date': x['date'], 'rawValue': x['rawValue']} for x in data]
        except:
            return []
        
    @token_required
    def get_ts(self, site, source, variable, interval=None):
        try:
            data = self.get_dps(site, source, variable=variable, interval=interval)
            dps = pd.DataFrame(data)
            dps = dps.sort_values(by="date")
            dps.index = pd.to_datetime(dps["date"], format=iso)
            dps["value"] = pd.to_numeric(dps["rawValue"], errors="coerce")
            return dps["value"]
        except:
            return None
        
    
    @token_required
    def push_dps(self, site, source, variable, dps=[]):
        logging.info(f"Opinum Datahub : pushing {len(dps)} datapoints to ({site}, {source}, {variable}) ...")
        return self.push([{
            'variableId': self.var(site, source, variable), 
            'data': dps
        }])
    
    @token_required
    def push_ts(self, site, source, variable, dps=None):
        try: 
            data = pd.DataFrame({ "date": dps.index.values, "value": dps.values })
            data["date"] = data["date"].dt.strftime(iso)
            data = data.to_dict(orient="records")
            return self.push_dps(site, source, variable=variable, dps=data)
        except: return