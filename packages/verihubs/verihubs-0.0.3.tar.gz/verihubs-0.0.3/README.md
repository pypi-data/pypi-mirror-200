# VeriHubs

Use our SMS API or Campaign Manager to send messages to all mobile phones globally. Verihubs’ comprehensive API and super network of direct operators makes it quick, easy, and secure.

### Send SMS OTP
```
from verihubs import Verihubs

v = Verihubs('your-app-id', 'your-secret')

response = v.send_sms_otp('628XXXXXXXX')

response.status_code
response.ok
response.json()
```


This package use requests, you can use same way like request

### Verify SMS OTP
```
from verihubs import Verihubs

v = Verihubs('your-app-id', 'your-secret')

response = v.verify_sms_otp('628XXXXXXXX', '1234')

response.status_code
response.ok
response.json()
```