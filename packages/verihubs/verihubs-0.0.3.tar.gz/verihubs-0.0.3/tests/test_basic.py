import unittest
from verihubs import VeriHubs


class BasicsTestCase(unittest.TestCase):

    def test_wrong_app_id(self):
        v = VeriHubs(app_id='something', api_key='something')
        response = v.send_sms_otp('628131101010110')
        self.assertEqual(response.status_code, 401)

    def test_true_app_id(self):
        v = VeriHubs(app_id='something', api_key='something')
        response = v.send_sms_otp('628131101010110')
        self.assertEqual(response.status_code, 401)

    
    def test_send_whatsapp_otp(self):
        v = VeriHubs(app_id='something', api_key='something')
        response = v.send_whatsapp_otp('628131101010110', lang_code='id', template='otp')
        self.assertEqual(response.status_code, 201)


    def test_verify_whatsapp_otp(self):
        v = VeriHubs(app_id='something', api_key='something')
        response = v.verify_whatsapp_otp('628131101010110', otp='558715')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()