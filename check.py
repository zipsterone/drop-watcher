import requests, json, os

URL = "https://justfitteds.com/collections/all/products.json?sort_by=created-descending&limit=20"
NTFY = "https://ntfy.sh/" + os.environ["NTFY_TOPIC"]
STATE = "seen.json"

seen = set(json.load(open(STATE))) if os.path.exists(STATE) else None
r = requests.get(URL, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
r.raise_for_status()
products = r.json()["products"]

if seen is not None:
    for p in products:
        if p["id"] not in seen:
            requests.post(NTFY, data=p["title"].encode("utf-8"), headers={
                "Title": "Neues Produkt",
                "Click": f"https://justfitteds.com/products/{p['handle']}",
                "Priority": "high",
            })

json.dump([p["id"] for p in products], open(STATE, "w"))
