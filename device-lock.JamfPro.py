import http.client

conn = http.client.HTTPSConnection("https://jss.eanesisd.net:8443")
payload = "<mobile_device_command><general><command>RestartDevice</command></general><mobile_devices><mobile_device><id>12341</id></mobile_device></mobile_devices></mobile_device_command>"
headers = {
'content-type': "application/xml",
'authorization': "username:password" #change username:password to match Jamf Pro credentials.
}
conn.request("POST", "/JSSResource/mobiledevicecommands/command", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
