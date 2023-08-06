import requests
from ra_engine.core.app import RAEApp, XAPIKey
from ra_engine.type_def.ml import TrainData, PredData, MLData, TSData
import pandas as pd
from ra_engine.type_def.results import Response


class EvaluatorML:
    def __init__(
        self,
        endpoint: str,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        self.rae_app: RAEApp = app
        self.ml_data = MLData(
            TrainData(train_df, features, targets, train_config),
            PredData(pred_df, pred_config),
        )
        self._app = app.app()
        self.endpoint = endpoint
        if self._app is None:
            raise ValueError("RAEApp is not initialized. Please run app.init() first.")
        if self._app.result is None:
            raise ValueError(
                "Provided RAEApp is not authenticated properly. Please check your credentials."
            )
        if self.rae_app.x_api_key is None:
            raise ValueError(
                "Provided RAEApp is not authenticated properly. API Key is not generated. Please run RAEApp.generate_api_key() first."
            )

    def exec(self) -> Response:
        self.response = requests.post(
            self.rae_app.credentials.host + self.endpoint,
            json=self.ml_data.as_dict(),
            headers={
                "Content-Type": "application/json",
                "X-Api-Key": f"{self.rae_app.x_api_key.key}",
            },
        )
        return Response(self.response)

    def inputs(self) -> dict:
        return self.ml_data.as_dict()


class EvaluatorTS:
    def __init__(
        self,
        endpoint: str,
        app: RAEApp,
        train_df: pd.DataFrame,
        dates_col: str,
        target_col: str,
        train_config: dict = None,
        forcast_for: int = 1,
    ):

        self.rae_app: RAEApp = app
        self.ts_data = TSData(
            train_df, dates_col, target_col, train_config, forcast_for
        )
        self._app = app.app()
        self.endpoint = endpoint
        self.response = None
        self._json = None
        if self._app is None:
            raise ValueError("RAEApp is not initialized. Please run app.init() first.")
        if self._app.result is None:
            raise ValueError(
                "Provided RAEApp is not authenticated properly. Please check your credentials."
            )
        if self.rae_app.x_api_key is None:
            raise ValueError(
                "Provided RAEApp is not authenticated properly. API Key is not generated. Please run RAEApp.generate_api_key() first."
            )

    def exec(self) -> Response:
        self.response = requests.post(
            self.rae_app.credentials.host + self.endpoint,
            json=self.ts_data.as_dict(),
            headers={
                "Content-Type": "application/json",
                "X-Api-Key": f"{self.rae_app.x_api_key.key}",
            },
        )
        return Response(self.response)

    def inputs(self) -> dict:
        return self.ts_data.as_dict()
