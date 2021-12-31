#!/usr/bin/env python3

import sys, json, logging, requests
from typing import Coroutine, Counter
from optparse import OptionParser
from requests import api


parser = OptionParser()
parser.add_option("-l", "--list", help="list the API changes before commiting", action="store_true", dest="list")
parser.add_option("-c", "--commit", help="[GET], [CHECK], [UPDATE], [POST], or [DELETE] the API changes", dest="commit")
parser.add_option("-t", "--TOKEN", help="Monster Alert API Token. Required when -c (--commit) flas is specified", dest="token")
(options, args) = parser.parse_args()

dynVarURL = "https://raw.github.factset.com/market-data-cloud/account_config/master/alerting/apiChanges.json"
dynVarHEADER = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
dynVarResponse = requests.get(dynVarURL, headers=dynVarHEADER)
(dynVarResponse.status_code, dynVarResponse.reason)
if dynVarResponse.status_code != 200:
    print("Dynamic variable parsing from GitHub Account Config repo, failed.")
    exit()
jsonRespDynVar = dynVarResponse.json()                                  

accountOwnerEmail = jsonRespDynVar["accountOwnerEmail"]
alertThresholds = jsonRespDynVar["alertThresholds"]
alertTypes = jsonRespDynVar["alertTypes"]

API_TOKEN = options.token
API_URL = "https://alerting-api.url.io/api/alert/timeseries/threshold"
HEADERS = {'Authorization' : "ALERTINGAPI apikey=\"" + API_TOKEN + "\""}

TotalQueries=len(accountOwnerEmail.keys()) * len(alertThresholds) * len(alertTypes.keys())

def apiList():
    for key in accountOwnerEmail:
        for th in alertThresholds:
            for ty in alertTypes:

                listPrint={"properties": [
                        {
                        "name": str("QuotesCloudAlert-Threshold." + ty.upper() + "." + str(th) + "." + key.lower().split(".")[1] + "." + key.lower().split(".")[2])
                        },
                        {
                        "env": key.lower().split(".")[2]
                        },
                        {
                        "account": key.lower()
                        },
                        {
                        "owner": accountOwnerEmail[key]
                        },
                        {
                        "threshold_type": ty.lower()
                        },
                        {
                        "threshold_value": str(th)
                        }
                    ]}
                print(listPrint)

def apiGet():
    apiGet.Counter = 1
    for key in accountOwnerEmail:
            for th in alertThresholds:
                for ty in alertTypes:
                    APIurlGet=str("https://alerting-api.url.io/api/alert/timeseries/QuotesCloudAlert-Threshold." + ty.upper() + "." + str(th) + "." + key.lower().split(".")[1] + "." + key.lower().split(".")[2])
                    responseGet = requests.get(APIurlGet, headers=HEADERS)
                    print(APIurlGet)
                    print(responseGet.status_code, responseGet.reason)
                    print(f"{responseGet.status_code} {responseGet.reason} {apiGet.Counter}/{TotalQueries}")
                    apiGet.Counter += 1

def apiCheck():
    apiCheck.Counter = 0
    for key in accountOwnerEmail:
            for th in alertThresholds:
                for ty in alertTypes:
                    APIurlCheck=str("https://alerting-api.url.io/api/alert/timeseries/QuotesCloudAlert-Threshold." + ty.upper() + "." + str(th) + "." + key.lower().split(".")[1] + "." + key.lower().split(".")[2])
                    responseCheck = requests.get(APIurlCheck, headers=HEADERS)
                    print(APIurlCheck)
                    print(responseCheck.status_code, responseCheck.reason)
                    print(f"{responseCheck.status_code} {responseCheck.reason} {apiCheck.Counter + 1}/{TotalQueries}")
                    if responseCheck.status_code == 200:            
                        apiCheck.Counter += 1

def apiDelete():
    apiDelete.Checker = 0
    apiDelete.Failures = 0
    apiDelete.Conflicts = 0
    Counter = 1
    for key in accountOwnerEmail:
            for th in alertThresholds:
                for ty in alertTypes:
                    APIurlDelete=str("https://alerting-api.url.io/api/alert/timeseries/QuotesCloudAlert-Threshold." + ty.upper() + "." + str(th) + "." + key.lower().split(".")[1] + "." + key.lower().split(".")[2])
                    responseDelete = requests.delete(APIurlDelete, headers=HEADERS)
                    print(APIurlDelete)
                    print(responseDelete.status_code, responseDelete.reason)
                    print(f"{responseDelete.status_code} {responseDelete.reason} {Counter}/{TotalQueries}")
                    Counter += 1
                    if responseDelete.status_code == 200:
                        apiDelete.Checker += 1
                    elif responseDelete.status_code == 404:
                        apiDelete.Conflicts += 1
                    else:
                        apiDelete.Failures += 1

def apiUpdate():
    apiUpdate.Checker = 0
    apiUpdate.Failures = 0
    apiUpdate.Conflicts = 0
    Counter = 1
    for key in accountOwnerEmail:
        for th in alertThresholds:
            for ty in alertTypes:
                if th >= 80:
                    alertSeverity = "CRITICAL"
                elif th >= 50:
                    alertSeverity = "WARNING"
                else:
                    alertSeverity = "INFO"
                DATAupdate={
                    "expression": "\"" + alertTypes[ty].lower() + "\"" + " >= " + str(th),
                    "thresholdType": "sustainedForXmins",
                    "duration": "3",
                    "violatedCount": "",
                    "aggregator": "first",
                    "enableGroupBy": True,
                    "alertConditions": "",
                    "alertName": "QuotesCloudAlert-Threshold." + ty.upper() + "." + str(th) + "." + key.lower().split(".")[1] + "." + key.lower().split(".")[2],
                    "owners": [
                        "GREENWICH\\quotes cloud"
                    ],
                    "isEnabled": True,
                    "alertPurpose": "Warn of potential service impact to market data as a result of insufficient resources",
                    "alertImpact":  ty.upper() + " utilization has crossed the pre-defined threshold.",
                    "alertStepsToFix": "Check the host or re-deploy the image.",
                    "properties": [
                        {
                        "key": "env",
                        "value": key.lower().split(".")[2]
                        },
                        {
                        "key": "account",
                        "value": key.lower()
                        },
                        {
                        "key": "owner",
                        "value": accountOwnerEmail[key]
                        },
                        {
                        "key": "threshold_type",
                        "value": ty.lower()
                        },
                        {
                        "key": "threshold_value",
                        "value": str(th)
                        }
                    ],
                    "database": "telegraf.standard",
                    "measurement": ty.lower(),
                    "deviceGroups": [],
                    "tags": [
                        {
                        "key": "alert_threshold_" + ty.lower(),
                        "value": str(th),
                        "filter": "=="
                        },
                        {
                        "key": "account_name",
                        "value": key.lower(),
                        "filter": "=="
                        }
                    ],
                    "groupBy": [
                        "account_name",
                        "autoscaling_group",
                        "alert_threshold_" + ty.lower(),
                        "host"
                    ],
                    "recipients": [],
                    "emailNotifications": [
                        {
                        "recipients": [
                            accountOwnerEmail[key]
                        ],
                        "disableClearNotification": False
                        }
                    ],
                    "opsGenieNotifications": [],
                    "rpdNotifications": [],
                    "webHookNotifications": [],
                    "holidayProfileGuid": "",
                    "timeProfileGuid": "9F44730C-3BB3-4BC4-A98F-E92DC03776F6",
                    "ignoreMaintenanceMode": False,
                    "alertLevel": alertSeverity,
                    "subject/title": "{{.TaskName}}: {{ index .Tags  \"autoscaling_group\" }} / {{ index .Tags  \"host\" }}",
                    "message": ty.upper() + " threshold has been crossed with the following details:<br>AWS Account: {{ index .Tags  \"account_name\" }}<br>Hostname: {{ index .Tags  \"host\" }}<br>Auto Scaling Group: {{ index .Tags  \"autoscaling_group\" }}<br>Alert   Threshold Level: {{ index .Tags  \"alert_threshold_" + ty.lower() +"\" }}"
                    }
                #print(json.dumps(DATA))         
                responseUpdate = requests.put(API_URL, headers=HEADERS, json=DATAupdate)
                print(f"{responseUpdate.status_code} {responseUpdate.reason} {Counter}/{TotalQueries}")
                Counter += 1
                if responseUpdate.status_code == 200:
                    apiUpdate.Checker += 1
                elif responseUpdate.status_code == 404:
                    apiUpdate.Conflicts += 1
                else:
                    apiUpdate.Failures += 1

def apiCommit(breaker=0):
    apiCommit.Checker = 0
    apiCommit.Failures = 0
    apiCommit.Conflicts = 0
    Counter = 1
    for key in accountOwnerEmail:
        for th in alertThresholds:
            for ty in alertTypes:
                if th >= 80:
                    alertSeverity = "CRITICAL"
                elif th >= 50:
                    alertSeverity = "WARNING"
                else:
                    alertSeverity = "INFO"
                DATA={
                    "expression": "\"" + alertTypes[ty].lower() + "\"" + " >= " + str(th),
                    "thresholdType": "sustainedForXmins",
                    "duration": "3",
                    "violatedCount": "",
                    "aggregator": "first",
                    "enableGroupBy": True,
                    "alertConditions": "",
                    "alertName": "QuotesCloudAlert-Threshold." + ty.upper() + "." + str(th) + "." + key.lower().split(".")[1] + "." + key.lower().split(".")[2],
                    "owners": [
                        "GREENWICH\\quotes cloud"
                    ],
                    "isEnabled": True,
                    "alertPurpose": "Warn of potential service impact to market data as a result of insufficient resources",
                    "alertImpact":  ty.upper() + " utilization has crossed the pre-defined threshold.",
                    "alertStepsToFix": "Check the host or re-deploy the image.",
                    "properties": [
                        {
                        "key": "env",
                        "value": key.lower().split(".")[2]
                        },
                        {
                        "key": "account",
                        "value": key.lower()
                        },
                        {
                        "key": "owner",
                        "value": accountOwnerEmail[key]
                        },
                        {
                        "key": "threshold_type",
                        "value": ty.lower()
                        },
                        {
                        "key": "threshold_value",
                        "value": str(th)
                        }
                    ],
                    "database": "telegraf.standard",
                    "measurement": ty.lower(),
                    "deviceGroups": [],
                    "tags": [
                        {
                        "key": "alert_threshold_" + ty.lower(),
                        "value": str(th),
                        "filter": "=="
                        },
                        {
                        "key": "account_name",
                        "value": key.lower(),
                        "filter": "=="
                        }
                    ],
                    "groupBy": [
                        "account_name",
                        "autoscaling_group",
                        "alert_threshold_" + ty.lower(),
                        "host"
                    ],
                    "recipients": [],
                    "emailNotifications": [
                        {
                        "recipients": [
                            accountOwnerEmail[key]
                        ],
                        "disableClearNotification": False
                        }
                    ],
                    "opsGenieNotifications": [],
                    "rpdNotifications": [],
                    "webHookNotifications": [],
                    "holidayProfileGuid": "",
                    "timeProfileGuid": "9F44730C-3BB3-4BC4-A98F-E92DC03776F6",
                    "ignoreMaintenanceMode": False,
                    "alertLevel": alertSeverity,
                    "subject/title": "{{.TaskName}}: {{ index .Tags  \"autoscaling_group\" }} / {{ index .Tags  \"host\" }}",
                    "message": ty.upper() + " threshold has been crossed with the following details:<br>AWS Account: {{ index .Tags  \"account_name\" }}<br>Hostname: {{ index .Tags  \"host\" }}<br>Auto Scaling Group: {{ index .Tags  \"autoscaling_group\" }}<br>Alert   Threshold Level: {{ index .Tags  \"alert_threshold_" + ty.lower() +"\" }}"
                    }
                #print(json.dumps(DATA))         
                response = requests.post(API_URL, headers=HEADERS, json=DATA)
                if breaker == 0: print(f"{response.status_code} {response.reason} {Counter}/{TotalQueries}")
                Counter += 1
                if response.status_code == 201:
                    apiCommit.Checker += 1
                elif response.status_code == 409:
                    apiCommit.Conflicts += 1
                elif response.status_code == 401:
                    print("Unauthorized access")
                    exit()
                else:
                    apiCommit.Failures += 1
                if breaker == 1: break
            if breaker == 1: break
        if breaker == 1: break
            

apiCommit(1)

if options.list == True:
    apiList()
    exit()

if options.commit == "UPDATE":
    proceed=input(f"{TotalQueries} queries will be updated, proceed? [YES|NO|LIST] ")
    if proceed == 'YES':
        apiUpdate()
        print(f"Resources Updated: {apiUpdate.Checker}/{TotalQueries}\nResources Don't Exist: {apiUpdate.Conflicts}/{TotalQueries}\nResource Update Failures: {apiUpdate.Failures}/{TotalQueries}")
    elif proceed == 'LIST':
        apiList()
    else:
        exit()

if options.commit == "POST":
    proceed=input(f"{TotalQueries} queries will be created, proceed? [YES|NO|LIST] ")
    if proceed == 'YES':
        apiCommit(0)
        print(f"New Resources Created: {apiCommit.Checker}/{TotalQueries}\nResources Already Exists: {apiCommit.Conflicts}/{TotalQueries}\nResource Creation Failures: {apiCommit.Failures}/{TotalQueries}")
    elif proceed == 'LIST':
        apiList()
    else:
        exit()

if options.commit == "GET":
    apiGet()
    print(f"{apiGet.Counter} API Get Requests were attempted")

if options.commit == "CHECK":
    apiCheck()
    if apiCheck.Counter == TotalQueries:
        print(f"Check passed, {apiCheck.Counter}/{TotalQueries} queries exists.")
     
if options.commit == "DELETE":
    proceedDelete=input(f"{TotalQueries} queries will be deleted, proceed? [YES|NO|LIST] ")
    if proceedDelete == "YES":
        apiDelete()
        print(f"Resources Deleted: {apiDelete.Checker}/{TotalQueries}\nResources Not Founds: {apiDelete.Conflicts}/{TotalQueries}\nResource Deletion Failures: {apiDelete.Failures}/{TotalQueries}")
    elif proceedDelete == 'LIST':
        apiList()
    else:
        exit()