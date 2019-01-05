import requests
from dataclasses import dataclass
from urllib.parse import quote
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SITE_DOMAIN 				= "https://riscocloud.com"
ELAS_WEBUI 					= "/ELAS/WebUI"
ELAS_WEBUI_SITELOGIN 		= ELAS_WEBUI + "/SiteLogin"
ELAS_WEBUI_SECURITY_GETCP 	= ELAS_WEBUI +"/Security/GetCPState"
ELAS_WEBUI_ARMED_ICON 		= ELAS_WEBUI + "/Content/images/ico-armed.png"
ELAS_WEBUI_SECURITY_ARMDIS	= ELAS_WEBUI + "/Security/ArmDisarm"
OK = 200


@dataclass
class AlarmGroup:
	id: int
	name: str
	armed: bool


class RiscoSession(object):
	def __init__(self):
		self.session = requests.Session()
		self.is_authenticated = False

	def get_cp_state(self) -> [AlarmGroup]:
		if not self.is_authenticated:
			raise Exception("Not Authenticated please call .authenticate(username, password, pin)")

		res = self.session.post(SITE_DOMAIN + ELAS_WEBUI_SECURITY_GETCP, verify=False)
		if res.status_code != OK:
			raise ValueError(f"Expected response to be 200 OK instead it was {status_code_stage_1}")

		data = res.json()
		if "detectors" not in data:
			raise ValueError("'detectors' is not in the response data this could be because you are calling this function too often please wait 30 seconds")

		if data["detectors"] is None or "parts" not in data["detectors"] or data["detectors"]["parts"] is None:
			raise ValueError("'parts' is not in the response data this could be because you are calling this function too often please wait 30 seconds")

		return self.__parse_detectors(data["detectors"]["parts"])

	def arm(self, id: int):
		return self.__arm_disarm(id, "armed")

	def disarm(self, id: int):
		return self.__arm_disarm(id, "disarmed")

	def __arm_disarm(self, id: int, action: str):
		if not self.is_authenticated:
			raise Exception("Not Authenticated please call .authenticate(username, password, pin)")

		form_payload = {
			"type": f"{id}:{action}",
			"passcode": "------",
			"bypassZoneID": -1
		}

		res = self.session.post(SITE_DOMAIN + ELAS_WEBUI_SECURITY_ARMDIS, 
								verify=False, 
								data=form_payload)

		if res.status_code != OK:
			raise ValueError(f"Expected response to be 200 OK instead it was {res.status_code}")

		return self.__parse_detectors(res.json()["detectors"]["parts"])

	def __parse_detectors(self, json_data: dict):
		return [AlarmGroup(id=x["id"],
							name=x["name"].strip(), 
							armed=x["armIcon"] == ELAS_WEBUI_ARMED_ICON)
				for x in json_data]


	def authenticate(self, username: str, password: str, pin: int):
		status_code_stage_1 = self.__stage_1().status_code
		if status_code_stage_1 != OK:
			raise ValueError(f"Expected response to be 200 OK instead it was {status_code_stage_1}")

		status_code_stage_2 = self.__stage_2(username, password).status_code
		if status_code_stage_2 != OK:
			raise ValueError(f"Expected response to be 200 OK instead it was {status_code_stage_2}")

		status_code_stage_3 = self.__stage_3(pin).status_code
		if status_code_stage_3 != OK: 
			raise ValueError(f"Expected response to be 200 OK instead it was {status_code_stage_3}")

		self.is_authenticated = True


	def __stage_1(self):
		res = self.session.get(SITE_DOMAIN + ELAS_WEBUI, verify=False)
		return res

	def __stage_2(self, username, password):
		form_payload = {
			"username": username,
			"password": password,
			"strRedirectToEventUID": "",
			"strRedirectToSiteId": ""
		}
		res = self.session.post(SITE_DOMAIN + ELAS_WEBUI, 
								data=form_payload, 
								verify=False)
		return res

	def __stage_3(self, pin: int):
		form_pyaload = {
			"SelectedSiteId": 1234,
			"Pin": pin
		}
		res = self.session.post(SITE_DOMAIN + ELAS_WEBUI_SITELOGIN,
								data=form_pyaload,
								verify=False)
		return res
