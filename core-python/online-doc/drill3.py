import requests
import os

token = os.getenv("API_TOKEN")
if not token:
    token = "abc"
class FlackyRequest:
    def __init__(self, req_url):
        self.req_url = req_url
    
    def get_url_response(self):
        headers = {"Authorization": f"Bearer {token}"}
        for i in range(3):
            try:
                response = requests.get(
                self.req_url,
                params={"page":1},
                headers=headers,
                timeout=5)
                response.raise_for_status()
                data = response.json()
                print(response.status_code)
                print(data, "compleated succesfully")
                break
            except requests.RequestException as e:
                print("try", type(e).__name__, e)
                if(i==2):
                    print("gave up")



if __name__ == "__main__":
    obj = FlackyRequest("https://httpbin.org/status/500")
    obj.get_url_response()