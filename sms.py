# -*- coding: utf-8 -*-
import requests
debug = False
def send_sms(
	             message):
    auth_token = "2b762f653c913c0589ed63c4e49cf848"
    account_sid = "AC070fcec7fa499dd1bab8a2734b0d9f70"
    if not debug:
        number_list = []
    else:
        number_list = []
    for recipient in number_list:
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = "To=" + recipient + "&From=" + "+18152611137" + "&Body=" + message
        print("Attempting to send SMS")
        r = requests.post("https://api.twilio.com/2010-04-01/Accounts/" +
                        account_sid + "/Messages.json",
                        data=data,
                        auth=(account_sid,auth_token),
                        headers=headers)
        if r.status_code >= 300 or r.status_code < 200:
            print("There was an error with your request to send a message. \n" +
                    "Response Status: " + str(r.status_code))
        else:
            print("Success")
            print(r.status_code)
        r.close()

message = "Juhuu wir sind reich baby!\nPermutation: "
send_sms(message)
