import requests
import healthcheckio.hc_log as hc_log

class ping():
    def __init__(self,uuid,api_key=None,*args,**kwargs):
        self.uuid=uuid
        self.api_key = api_key
        self.log = hc_log.log('HealthCheck.PING',debug=False)
        self.log.debug(f'Loading PING Object for {self.uuid}')
        self.BASE_URL='https://hc-ping.com/'
        self.START_FLAG='/start'
        self.ERROR_FLAG='/fail'
        self.LOG_FLAG='/log'
        self.session = requests.Session()
        self.headers = {}
        self.headers['User-Agent'] = 'HealthCheckIOAPI_1.0.0'
        if not api_key is None:
            self.log.debug(f'Found API KEY configuration, setting up API KEY for {self.uuid}.')
            self.headers['X-Api-Key'] = self.api_key
        self.session.headers = self.headers
        self.log.debug(f'Using Headers: {self.headers}')
        self.log.debug(f'New PING Object Loaded for {self.uuid}.')


    def ping_start(self):
        self.log.debug(f'Received request to send a START PING for {self.uuid}.')
        url = self.BASE_URL + self.uuid + self.START_FLAG
        try:
            resp = self.session.get(url)
        except requests.RequestException as e:
            t = f'FAIL: {e}'
            return t
        if resp.status_code == 200:
            t = 'SUCCESS: 200'
            return t
        else:
            t = 'FAIL: Invalid Request.'
            return t

    def ping_error(self):
        self.log.debug(f'Received request to send a FAIL PING for {self.uuid}.')
        url = self.BASE_URL + self.uuid + self.ERROR_FLAG
        try:
            resp = self.session.get(url)
        except requests.RequestException as e:
            t = f'FAIL: {e}'
            return t
        if resp.status_code == 200:
            t = 'SUCCESS: 200'
            return t
        else:
            t = 'FAIL: Invalid Request.'
            return t

    def ping_log(self,send_data):
        self.log.debug(f'Received request to send a LOG PING for {self.uuid}.')
        url = self.BASE_URL + self.uuid + self.LOG_FLAG
        try:
            resp = self.session.post(url,data=send_data)
        except requests.RequestException as e:
            t = f'FAIL: {e}'
            return t
        if resp.status_code == 200:
            t = 'SUCCESS: 200'
            return t
        else:
            t = 'FAIL: Invalid Request.'
            return t

    def ping_send(self):
        self.log.debug(f'Received request to send a SUCCESS PING for {self.uuid}.')
        url = self.BASE_URL + self.uuid
        try:
            resp = self.session.get(url)
        except requests.RequestException as e:
            t = f'FAIL: {e}'
            return t
        if resp.status_code == 200:
            t = 'SUCCESS: 200'
            return t
        else:
            t = 'FAIL: Invalid Request.'
            return t