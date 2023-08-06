from ra_engine.core.app import RAEApp
import pandas as pd
from ra_engine.ml.evaluators import EvaluatorML

base = "/api/v1/ml/classification"


class ANNCf(EvaluatorML):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        super().__init__(
            f"{base}/ann",
            app,
            train_df,
            pred_df,
            features,
            targets,
            train_config,
            pred_config,
        )


class GradientBoostingCf(EvaluatorML):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        super().__init__(
            f"{base}/gradboost",
            app,
            train_df,
            pred_df,
            features,
            targets,
            train_config,
            pred_config,
        )


class NaiveBayesCf(EvaluatorML):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        super().__init__(
            f"{base}/naivebayes",
            app,
            train_df,
            pred_df,
            features,
            targets,
            train_config,
            pred_config,
        )


class RandomForestCf(EvaluatorML):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        super().__init__(
            f"{base}/randomforest",
            app,
            train_df,
            pred_df,
            features,
            targets,
            train_config,
            pred_config,
        )


class SVMCf(EvaluatorML):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        super().__init__(
            f"{base}/svm",
            app,
            train_df,
            pred_df,
            features,
            targets,
            train_config,
            pred_config,
        )
