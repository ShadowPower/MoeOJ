import urllib.request
import json


def run(language, _input, code):
    url = "http://compiler.run/api/run"
    data = {
        "language": language,
        "language_v": "default",
        "input": _input,
        "code": code,
        "client": "web"
    }
    data = bytes(json.dumps(data), 'utf8')
    header = {
        "Referer": "http://complier.run",
        "Host": "complier.run",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "Content-Type": "application/json;charset=utf-8",
    }
    request = urllib.request.Request(url=url, headers=header, method="POST")
    res = urllib.request.urlopen(request, data, timeout=20)
    result = json.loads(res.read().decode("utf8"))
    return result
