import requests
import base64
import json
import time
from bs4 import BeautifulSoup

headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78", "cookie": "__yjs_duid=1_5c210f5ff94b0e0a984a67ab8d3dedb91675824675873; MCMOD_SEED=ja3351rh3hl9jpctueqen5mlv2; yjs_js_security_passport=5fa58090cd7d5791ddce359e270b38213541ed78_1675834846_js", "x-forwarded-for": "120.197.179.166"}

def finded_string(a: str, b: str) -> bool:
	return a.find(b) >= 0

def find_source(url: str) -> dict:
	req = requests.get(url, headers=headers)

	print("response: " + str(req.status_code))
	while (req.status_code >= 400 and not req.status_code == 404):
		print("retried: " + str(req.status_code))
		req = requests.get(url, headers=headers)

	if (req.status_code <= 399):
		soup: BeautifulSoup = BeautifulSoup(req.content, "html.parser")

		title = soup.find("div", attrs={"class": "class-title"})
		cnTitle = title.h3
		enTitle = title.h4
		result = {}
		result_fabric = {}

		offical = None
		mcbbs = None

		hasFabricVer = False

		try:
			for i in soup.find("ul", attrs={"class": "common-link-icon-frame common-link-icon-frame-style-3"}).find_all("li"):
				temp_tag = i.find("a")

				linkTitle = temp_tag.get("data-original-title")
				try:
					urlbase = str(base64.b64decode(temp_tag.get("href").split("/")[-1]), "utf-8")
				except (BaseException) as e:
					continue

				section = linkTitle.split(":")[0].lower()
				if (finded_string(section, "modrinth") or finded_string(section, "curseforge") or finded_string(section, "github") or finded_string(section, "mcarchive")):
					isNotGithub = not finded_string(section, "github")
					if (": Forge" in linkTitle):
						result[section] = urlbase
						if (isNotGithub):
							result["modid"] = urlbase.split("/")[-1]
					elif (linkTitle.find(": Fabric/Quilt") >= 0 or linkTitle.find(": Fabric") >= 0):
						result_fabric[section] = urlbase
						hasFabricVer = True
						if (isNotGithub):
							result_fabric["modid"] = urlbase.split("/")[-1]
					else:
						result[section] = urlbase
						if (isNotGithub):
							result["modid"] = urlbase.split("/")[-1]

				if (linkTitle.startswith("官方")):
					offical = urlbase

				if (linkTitle.startswith("MCBBS")):
					mcbbs = urlbase

		except (BaseException) as e:
			final2 = {}
			final2["mcmod"] = url
			if (enTitle == None):
				final2["name"] = {"en": cnTitle.string}
			else:
				final2["name"] = {"en": enTitle.string, "cn": cnTitle.string}

			return final2


		final = {}
		final["mcmod"] = url
		if (enTitle == None):
			final["name"] = {"en": cnTitle.string}
		else:
			final["name"] = {"en": enTitle.string, "cn": cnTitle.string}

		final["offical"] = offical
		final["mcbbs"] = mcbbs
		final["metadata"] = {}

		final["metadata"]["main"] = result
		if (hasFabricVer):
			final["metadata"]["fabric"] = result_fabric

		return final


# https://www.mcmod.cn/class/2021.html
if __name__ == "__main__":
	r = []
	for i in range(2, 9500):
		try:
			print("try accessing page " + str(i))
			item = find_source("https://www.mcmod.cn/class/" + str(i) + ".html")
			if (item != None):
				r.append(item)
				print("page " + str(i) + " successed")
		except (BaseException) as e:
			print(e)
	time.sleep(0.1)

	with open("mods_info.json", 'w', encoding='utf-8') as f:
		json.dump(r, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
