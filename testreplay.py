import requests, json

s = requests.Session()
r = s.get("https://play.pokemonshowdown.com")
print(r.text)
payload = {"name":"Lumaris", "pass":"Sh1ft3dpl@y","act":"login"}
r = s.post("https://play.pokemonshowdown.com/~~showdown/action.php", payload)
print(r.text)