import pandas as pd


class TrainData:
    def __init__(
        self, data: pd.DataFrame, features: list, targets: list, config: dict = None
    ):
        self.data: dict = data.to_dict()
        self.features: list = features
        self.targets: list = targets
        self.config: dict = config

    def as_dict(self):
        return {
            "data": self.data,
            "features": self.features,
            "targets": self.targets,
            "config": self.config,
        }


class TSData:
    def __init__(
        self,
        data: pd.DataFrame,
        dates_col: str,
        target_col: str,
        config: dict = None,
        forcast_for: int = 1,
    ):
        self.data: dict = data.to_dict()
        self.dates_col: str = dates_col
        self.target_col: str = target_col
        self.config: dict = config
        self.forcast_for: int = forcast_for

    def as_dict(self):
        return {
            "train": {
                "data": self.data,
                "dates_col": self.dates_col,
                "target_col": self.target_col,
                "config": self.config,
            },
            "forcast_for": self.forcast_for,
        }


class PredData:
    def __init__(self, data: pd.DataFrame, config: dict = None):
        self.data: dict = data.to_dict()
        self.config: dict = config

    def as_dict(self):
        return {"data": self.data, "config": self.config}


class MLData:
    def __init__(self, train: TrainData, predict: PredData):
        self.train: TrainData = train
        self.predict: PredData = predict

    def as_dict(self):
        return {"train": self.train.as_dict(), "predict": self.predict.as_dict()}
