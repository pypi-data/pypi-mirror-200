import pandas as pd


class Response:
    def __init__(self, response):
        self.response = response

    def __repr__(self):
        return f"Response(response={self.response})"

    def response(self):
        return self.response

    def status_code(self):
        return self.response.status_code

    def json(self):
        return self.response.json()

    def text(self):
        return self.response.text

    def result(self, as_df=False):
        _json = self.json()
        if _json:
            if _json.get("success", False):
                res = self.response.json().get("result", None)
                if res and as_df:
                    return pd.DataFrame(res)
                else:
                    return res
            else:
                raise Exception(
                    "No predictions available. Reason: " + _json.get("error", None)
                )
        else:
            raise Exception("No predictions available. Something went wrong.")

    def scores(self):
        return self.json().get("score", None)
