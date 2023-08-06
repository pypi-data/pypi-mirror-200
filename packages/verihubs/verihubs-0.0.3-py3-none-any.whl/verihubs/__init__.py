import requests


class VeriHubs:

    def __init__(self, app_id: str, api_key: str) -> None:
        self.app_id = app_id
        self.api_key = api_key
        self.base_url = 'https://api.verihubs.com/v1'

    
    @property
    def headers(self):
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        headers['App-ID'] = self.app_id
        headers['API-Key'] = self.api_key
        return headers
    

    def send_sms_otp(self, phone: str, template: str = None, expired: int = 300):
        """This method helps you to generate and send sms containing one-time password to destination number"""
        url = self.base_url + '/otp/send'
        payload = {'msisdn': phone, 'time_limit': expired}
        if template is not None:
            payload['template'] = template
        r = requests.post(
            url,
            headers=self.headers,
            json=payload)
        return r
    

    def verify_sms_otp(self, phone: str, otp: str):
        """This method helps you to verify one-time password to destination number"""
        url = self.base_url + '/otp/verify'
        payload = {'msisdn': phone, 'otp': otp}
        r = requests.post(
            url,
            headers=self.headers,
            json=payload)
        return r
    

    def send_flash_call(self, phone: str, expired: int = 120):
        """This method helps you to generate and send call containing one-time password to destination number"""
        url = self.base_url + '/flashcall/send'
        payload = {'msisdn': phone, 'time_limit': expired}
        r = requests.post(
            url,
            headers=self.headers,
            json=payload)
        return r
    
    
    def verify_flash_call(self, phone: str, otp: str):
        """This method helps you to verify one-time password to destination number"""
        url = self.base_url + '/flashcall/verify'
        payload = {'msisdn': phone, 'otp': otp}
        r = requests.post(
            url,
            headers=self.headers,
            json=payload)
        return r
    

    def send_whatsapp_otp(
            self, 
            phone: str,
            lang_code: str,
            template: str, 
            otp_length: str = '6',
            content: list = None,
            expired: int = 120):
        """This method helps you to generate and send Whatsapp message containing one-time password to destination number"""
        url = self.base_url + '/whatsapp/otp/send'
        payload = {
            'msisdn': phone,
            'content': content,
            'lang_code': lang_code,
            'template_name': template,
            'otp_length': otp_length,
            'time_limit': expired
            }
        r = requests.post(
            url,
            headers=self.headers,
            json=payload)
        return r
    

    def verify_whatsapp_otp(self, phone: str, otp: str):
        """This method helps you to verify one-time password to destination number"""
        url = self.base_url + '/whatsapp/otp/verify'
        payload = {'msisdn': phone, 'otp': otp}
        r = requests.post(
            url,
            headers=self.headers,
            json=payload)
        return r