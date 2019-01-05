# Research
# Auth Flow

| Method  | URL  | Data  | Response |
|---|---|---|---|
|  GET | /ELAS/WebUI  |   | You get the ASP.NET_SessionId cookie  |
| POST  | /ELAS/WebUI  | you need the ASP.NET_SessionId in your cookies and a http form body that looks like this: ```username=a@b.com&password=secret&strRedirectToEventUID=&strRedirectToSiteId=```  | a cookie named RUCookie that you need for further authentication |
| POST  |  /ELAS/WebUI/SiteLogin | you need both the ASP.NET_SessionId and RUCookie ```SelectedSiteId=****&Pin=****```  |  Nothing |


# You Must Be Authenticated

To do any of the following you must be authenticated meaning you must have the ASP.NET_SessionId and RUCookie inside youre cookiejar.


# Arm / Disarm
| Method  | URL  | Data  | Response |
|---|---|---|---|
| POST | /ELAS/WebUI/Security/ArmDisarm  |  The ASP.NET_SessionId and RUCookie must be included in your cookies and the form data should look like this: ```type=<id>:<arm/disarm>&passcode=&bypassZoneID=-1``` | a json object that represents your detectors  |


# Get Detector State
| Method  | URL  | Data  | Response |
|---|---|---|---|
| POST | /ELAS/WebUI/Security/GetCPState  | The ASP.NET_SessionId and RUCookie must be included in your cookies | a json object that represents your detectors  |