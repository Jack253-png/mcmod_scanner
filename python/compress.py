import json

if __name__ == "__main__":
	data = json.load(open("mods_info.json", "r", encoding="utf-8"))
	for item in data:
		if "mcbbs" in item and item["mcbbs"] == None:
			item.pop("mcbbs")
		if "offical" in item and item["offical"] == None:
			item.pop("offical")

		if "metadata" in item and len(item["metadata"]["main"].keys()) == 0:
			item["metadata"].pop("main")


	with open("mods_info_compressed.json", 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False)