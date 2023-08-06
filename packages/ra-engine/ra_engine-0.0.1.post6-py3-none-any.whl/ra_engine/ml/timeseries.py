from ra_engine.core.app import RAEApp
import pandas as pd
from ra_engine.ml.evaluators import EvaluatorTS

base = "/api/v1/ml/time-series"


class ARIMA(EvaluatorTS):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        dates_col: str,
        target_col: str,
        train_config: dict = None,
        forcast_for: int = 1,
    ):
        super().__init__(
            f"{base}/arima",
            app,
            train_df,
            dates_col,
            target_col,
            train_config,
            forcast_for,
        )


class AutoARIMA(EvaluatorTS):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        dates_col: str,
        target_col: str,
        train_config: dict = None,
        forcast_for: int = 1,
    ):
        super().__init__(
            f"{base}/auto-arima",
            app,
            train_df,
            dates_col,
            target_col,
            train_config,
            forcast_for,
        )


class Theta(EvaluatorTS):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        dates_col: str,
        target_col: str,
        train_config: dict = None,
        forcast_for: int = 1,
    ):
        super().__init__(
            f"{base}/theta",
            app,
            train_df,
            dates_col,
            target_col,
            train_config,
            forcast_for,
        )
