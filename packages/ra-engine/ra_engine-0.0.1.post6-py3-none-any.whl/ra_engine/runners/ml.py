import pandas as pd
from typing import Union
from ra_engine.core.app import RAEApp
import requests
from ra_engine.type_def.results import Response
from ra_engine.core.app import App


class SKLRunner:
    rae_app: RAEApp = None
    pred_df: pd.DataFrame = None
    pred_config: Union[dict, None] = None
    endpoint: str = "/api/v1/runner/skl"
    _app: App = None

    def __init__(
        self, app: RAEApp, pred_df: pd.DataFrame, pred_config: Union[dict, None] = None
    ):
        self.rae_app: RAEApp = app
        self.pred_df = pred_df
        self.pred_config = pred_config
        self._app: App = app.app()
        if self._app is None:
            raise ValueError("RAEApp is not initialized. Please run app.init() first.")
        if self._app.result is None:
            raise ValueError(
                "Provided RAEApp is not authenticated properly. Please check your credentials."
            )

    def inputs(self) -> dict:
        return {
            "data": self.pred_df.to_dict(),
            "config": self.pred_config,
        }

    def exec(self, id: str):
        response = requests.get(
            self.rae_app.credentials.host + self.endpoint + f"/{id}",
            json=self.inputs(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._app.result['jwt']}",
            },
        )
        return Response(response)
