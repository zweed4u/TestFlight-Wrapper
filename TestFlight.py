#!/usr/bin/python3

import json
import requests

class TestFlight:
    def __init__(self, session_id, session_digest, request_id):
        self.session = requests.session()
        self.session_id = session_id
        self.session_digest = session_digest
        self.request_id = request_id
        self.base_url = 'https://beta.itunes.apple.com/v1/'
        self.headers = {
            'Host':              'beta.itunes.apple.com',
            'Content-Type':      'application/json',
            'Cookie':            'dc=st',
            'X-Session-Id':      self.session_id,
            'Connection':        'keep-alive',
            'Accept':            'application/json',
            'X-Session-Digest':  self.session_digest,
            'User-Agent':        'Oasis/2.0.0 iOS/10.2 model/iPhone6,1 hwp/s5l8960x build/14C92 (6; dt:89)',
            'X-Request-Id':      self.request_id,
            'Accept-Language':   'en-us',
            'Accept-Encoding':   'gzip, deflate'
        }

    def _make_request(self, method, path, params=None, data=None, json=None, headers=None):
        return self.session.request(method, f'{self.base_url}{path}', params=params, data=data, json=json, headers=headers).json()

    def get_devices(self):
        return self._make_request('GET', 'devices', headers=headers)

    def get_account_apps(self, account_uuid):
        return self.session.request('GET', f'https://beta.itunes.apple.com/v3/accounts/{account_uuid}/apps', headers=headers).json()

    def redeem_code(self, redeem_code):
        return self._make_request('POST', f'invites/code/{str(redeem_code).upper()}/redeem', headers=headers)

    def stop_testing_app(self, app_id):
        return self._make_request('POST', f'apps/{str(app_id)}/withdraw', headers=headers)

    def get_app_overview(self, app_id):
        return self._make_request('GET', f'accounts/settings/notifications/apps/{str(app_id)}', headers=headers)

    def get_app_previous_versions(self, account_uuid, app_id):
        return self.session.request('GET', f'https://beta.itunes.apple.com/v2/accounts/{account_uuid}/apps/{str(app_id)}/platforms/ios/trains', headers=headers).json()

    def get_app_previous_version_builds(self, account_uuid, app_id, version):
        return self.session.request('GET', f'https://beta.itunes.apple.com/v2/accounts/{account_uuid}/apps/{str(app_id)}/platforms/ios/trains/{str(version)}/builds', headers=headers).json()

    def get_app_notifications(self, app_id):
        return self._make_request('GET', f'accounts/settings/notifications/apps/{str(app_id)}', headers=headers)

    def set_app_notifications(self, app_id, is_mobile, is_email):
        payload = {
            "appAdamId": str(app_id),
            "name": "",
            "platformUpdates": {
                "appletvos": {
                    "emailEnabled": True,
                    "name": "appletvos",
                    "productName": "",
                    "pushEnabled": True
                },
                "ios": {
                    "emailEnabled": is_email,
                    "name": "ios",
                    "productName": "",
                    "pushEnabled": is_mobile
                }
            }
        }
        return self._make_request('POST', f'accounts/settings/notifications/apps/{str(app_id)}', json=payload, headers=headers)

    def remove_device(self, vendor_id):
        payload = {
            "devices": [
                {
                    "vendorId": str(vendor_id).upper()
                }
            ]
        }
        return self._make_request('POST', f'devices/remove', json=payload, headers=headers)



TF = TestFlight('', '', '')
print(TF.get_devices())
print(TF.redeem_code(''))
print(TF.stop_testing_app())
print(TF.get_account_apps(''))
print(TF.get_app_overview())
print(TF.get_app_previous_versions('', ))
print(TF.get_app_previous_version_builds('', , ))
print(TF.set_app_notifications(, , ))
print(TF.get_app_notifications())
print(TF.remove_device(''))
