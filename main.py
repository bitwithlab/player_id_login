import os
import time
import requests
from fastapi import FastAPI, HTTPException
os.system("cls")

app = FastAPI()
session = requests.Session()
@app.get("/api/player_id_login")
def player_id_login(login_id: str):
    print(f"Received login_id: {login_id}")
    
    get_date_token = session.post(
        "https://datadome.garena.com/js/",
        headers={"referer": "https://shop.garena.sg/",
            "origin": "https://shop.garena.sg",
            "content-type": "application/x-www-form-urlencoded"},
        data={"ddk": "AE3F04AD3F0D3A462481A337485081"},
        timeout=10,
    )
    dd_cookie = get_date_token.json().get('cookie').split(';')[0].replace('datadome=', '')
    print(f"Received dd_cookie: {dd_cookie}")
    json_data = {'app_id': 100067,'login_id': login_id,}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'https://shop.garena.my',
        'Referer': 'https://shop.garena.my/?channel=202953',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Google Chrome";v="157", "Chromium";v="157"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',}
    response = requests.post('https://shop.garena.my/api/auth/player_id_login' , cookies={'region': 'MY',
            'language': 'en',
            'source': 'pc',
            "datadome": dd_cookie
            }, headers=headers , json=json_data)
    resp_json = response.json()
    print(f"Response JSON: {resp_json}")
    nickname = resp_json.get("nickname")
    if 'https://geo.captcha-delivery.com' in response.text:
        return {"error": "Captcha required"}
    if not nickname:
            return {"error": "Nickname not found"}
    if resp_json.get("region") != "BD":
        return {"error": "Invalid region"}
    return {"nickname": nickname,
            "player_id": login_id,
             "cookies": "" + ";".join([f"{key}={value}" for key, value in response.cookies.get_dict().items()]),
             "timestamp": int(time.time())
             }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
