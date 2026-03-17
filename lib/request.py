import requests

from secrets import API_KEY, DEVICE_ID

class Requester:

    def __init__(self, url: str):
        self.headers: dict = {
            "Content-Type": "application/json",
            "X-API-KEY": API_KEY,
            "X-Device-Id": DEVICE_ID,
        }
        self.kwargs: dict = {}
        self.url: str = url

    def post(self, data: dict) -> dict | None:
        self.kwargs = {"headers": self.headers, "json": data}
        return self.__make_request("POST")

    def __make_request(self, method: str = "GET"):
        try:
            response = requests.request(method, self.url, **self.kwargs)
            try:
                result = response.json()
            except ValueError:
                result = response.text

            return {
                "status": response.status_code,
                "data": result
            }
        except OSError as os_error:
            return {
                'status': 500,
                'error': 'Network error',
                'detail': str(os_error),
                'type': 'OSError'
            }
        except ValueError as value_error:
            return {
                'status': 400,
                'error': 'Invalid request',
                'detail': str(value_error),
                'type': 'ValueError'
            }
        except BaseException as error:
            return {
                'status': 500,
                'error': 'Unknown error',
                'detail': str(error),
                'type': type(error).__name__
            }
        finally:
            if "response" in locals():
                response.close()
