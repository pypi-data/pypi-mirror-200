from ra_engine.type_def.creds import Credentials
import requests
from typing import Union


class XAPIKey:
    key = None

    def __init__(self, key: str):
        self.key = key


class RAEApp:
    def __init__(self, credentials: Credentials, debug=False):
        self.credentials = credentials
        self.debug = debug
        self._app: App = None
        self.x_api_key: XAPIKey = None

    def init(self):
        response = requests.post(
            self.credentials.host + "/auth/login",
            json={
                "email": self.credentials.email,
                "password": self.credentials.password,
            },
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 200:
            self._app = App(**response.json())
        return response

    def ping(self):
        response = requests.get(self.credentials.host + "/ping")
        return response

    def app(self):
        return self._app

    def generate_api_key(self, name: str, expire_in: int = 30) -> XAPIKey:
        response = requests.post(
            self.credentials.host + "/auth/token/api/new",
            json={
                "name": name,
                "expire_in": expire_in,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._app.result['jwt']}",
            },
        )
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get("success", False):
                self.x_api_key = XAPIKey(res_json.get("result", None)["X-Api-Key"])
                return self.x_api_key
            else:
                raise Exception(res_json.get("error", None))
        else:
            raise Exception("Something went wrong.")


class User:
    def __init__(
        self,
        uid,
        first_name,
        last_name,
        email,
        tel,
        created_ts,
        updated_ts,
        last_login_ts,
    ):
        self.uid: str = uid
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.tel: str = tel
        self.created_ts: str = created_ts
        self.updated_ts: Union[str, None] = updated_ts
        self.last_login_ts: Union[str, None] = last_login_ts


class AuthResult:
    def __init__(self, jwt: str, user: User, generated_ts: float):
        self.jwt: str = jwt
        self.user: User = user
        self.generated_ts: float = generated_ts


class App:
    def __init__(self, success: bool, msg: str, result: AuthResult):
        self.success = success
        self.msg = msg
        self.result: Union[AuthResult, None] = result
