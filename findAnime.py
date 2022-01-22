import requests

jikanApiBase = "https://api.jikan.moe/v3"
def findAnime(searchQuery, limit):
    url = f"{jikanApiBase}/search/anime?q={searchQuery}&limit={limit}"
    req = requests.get(url)
    res = req.json()
    return res
print(findAnime("Tsuritama", 5))
