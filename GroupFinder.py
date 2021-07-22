import requests
import json
from discord import Webhook, RequestsWebhookAdapter # You don't have to use a webhook, but it makes it cleaner.

min = 44444
max = 44455 # Feel free to set this to whatever you want, but issues arise with big ranges
iteration = max - min

# There will be issues with big ranges, like mentioned above, I have a solution in the works, but I want to use threading...
# Notice, how I didn't use any try: or except:, its cause I wanted a headache debugging this crap...

def produceURL(min, max): # This will provide the URL we need to use the API to check all the Groups
    GrpURL = 'https://groups.roblox.com/v2/groups?groupIds='
    for i in range(min, max+1):
        if i != max:
            GrpURL = GrpURL + str(i) + ","
        else:
            GrpURL = GrpURL + str(i)
    print(GrpURL)
    return GrpURL

def getResp(GrpURL): # This is the parsing function that was written in about 2 minutes, so its probably garbage.
    ReqResponse = requests.get(GrpURL)
    ResponseDict = json.loads(ReqResponse.text) # Variable initilization
    for i in range(0, iteration+1): # Iterate over the amount of dictionaries in the data from ROBLOX
        for key, value in ResponseDict['data'][i].items(): # Honestly, useless way to check all this crap, but it made it easier for the None type
            if key == "owner": # Check if the key is owner
                if value is None: # If the value of the key is None type
                    print("Oh shit...")
                    if isItClosed(ResponseDict['data'][i]['id']) == True: # It sends it off to the function to be checked if you can join it, if so ping a webhook.
                        sendMessage(ResponseDict['data'][i]['id'])
                        print("Ding ding ding, check your webhook...")
                    else:
                        print("Nevermind...")
                else:
                    print("Just keep swimming...")

def isItClosed(id): # We will check if you can even join the group...
    ReqResponse = requests.get('https://groups.roblox.com/v1/groups/' + str(id))
    ResponseDict = json.loads(ReqResponse.text)
    for key, value in ResponseDict.items(): # Just checking to see if I can join...
        if key == "publicEntryAllowed":
            bool = value # Store the value as some crappy term to return
    return bool # Oh, hey look a boolean value!

def sendMessage(id):
    webhook = Webhook.from_url("insert your webhook here", adapter=RequestsWebhookAdapter()) # Need to insert your own webhook.
    webhook.send("https://www.roblox.com/groups/" + str(id)) # It will provide the group-link for ease of use.





if __name__ == "__main__": # Just so if you somehow can make this into a library for degenerates...
    GrpURL = produceURL(min, max)
    getResp(GrpURL)
