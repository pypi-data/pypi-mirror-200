import os
from typing import List, Optional

import pandas as pd
import requests

from eigenrules.exceptions import raise_missing_argument, raise_not_implemented
from eigenrules.schemas import (
    Data,
    FeatureImportance,
    Prediction,
    PredictRequest,
    RuleEvalRequest,
    Rules,
    decode_data,
    encode_data,
)


class RulesEngine:
    def __init__(self, api_token: str, api_url: Optional[str] = "https://api.eigendata.ai", api_version="v1") -> None:
        self.token = os.getenv("EIGEN_API_TOKEN", api_token)
        self.api_url = api_url
        self.api_version = api_version
        self.dataset: pd.DataFrame = None
        self.data: Data = None
        self.model_id: int = None

    def _load_data(self, path: Optional[str], data: Optional[pd.DataFrame]):
        if data is not None:
            self.dataset = data
        elif path is not None:
            self.dataset = pd.read_csv(path)
        else:
            raise_missing_argument()

    def train(
        self,
        name: str,
        data_path: Optional[str],
        target: str,
        control_class: str | int,
        features: Optional[List[str]],
        data: Optional[pd.DataFrame] = None,
        split: Optional[float] = 0.25,
        balance: Optional[float] = 0,
        complexity: Optional[int] = 10,  # from 1 to 32
    ) -> int:
        """
        Returns the trained model id. Sets this model as default for the RulesEngine class.

        Parameters
        ----------
        name : str
            Name identifier for the model..
        data_path : str
            Path to dataset (CSV). Required unless `data` argument is provided.
        data : pd.DataFrame, Optional
            pandas DataFrame object containing the dataset.
        target : str
            Name of the Target column.
        control_class : str | int
            One of the target classes. Required for metric generation purposes.
        split : float, Optional
            Which percentage of the dataset to be used for testing. > 0 and < 1.
        balance : float, Optional
            Value between 0 and 1 that balances the dataset classes during training sampling.
        complexity : int, Optional
            the higher this value the more complex the rules we can generate. Caps at 32.


        Returns
        -------
        model_id : int
            Trained model id for future use. This gets set as default use within the class instance.
        """
        train_url = f"{self.api_url}/{self.api_version}/models/train"
        headers = {"Authorization": f"Bearer {self.token}"}

        self._load_data(data_path, data)

        data = Data(
            name=name,
            dataset=encode_data(self.dataset),
            target=target,
            control_class=control_class,
            features=features,
            balance=balance,
            split=split,
            max_depth=complexity,
        )

        self.data = data

        response = requests.post(url=train_url, headers=headers, json=data.dict())
        self.model_id = response.json()["id"]
        return response.json()["id"]

    def authenticate(self, username: str, password: str):
        auth_url = f"{self.api_url}/token"
        form_data = {"username": username, "password": password}
        res = requests.post(auth_url, data=form_data)
        self.token = res.json()["access_token"]

    def get_rules(self, model_id: Optional[int] = None) -> Rules:
        gen_rules_url = f"{self.api_url}/{self.api_version}/rules/gen"
        headers = {"Authorization": f"Bearer {self.token}"}
        self.data.model_id = model_id or self.model_id
        res = requests.post(gen_rules_url, headers=headers, json=self.data.dict())
        res = res.json()
        rules = Rules(rule_set=decode_data(res["rule_set"]), importance=decode_data(res["importance"]))
        return rules

    def list_models(self) -> pd.DataFrame:
        list_models = f"{self.api_url}/{self.api_version}/models"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        res = requests.get(url=list_models, headers=headers)
        models = res.json()
        return pd.DataFrame.from_dict(models)

    def predict(self, datapoint: pd.DataFrame, model_id: Optional[int] = None) -> Prediction:
        mid = model_id or self.model_id
        predict_url = f"{self.api_url}/{self.api_version}/models/{mid}/predict"
        req = PredictRequest(datapoint=encode_data(datapoint), model_id=mid)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        res = requests.post(predict_url, headers=headers, json=req.dict())
        res_json = res.json()
        prediction = Prediction(
            datapoint=datapoint,
            result=decode_data(res_json["result"]),
            confidence=decode_data(res_json["confidence"]),
        )
        return prediction

    def explain(self, model_id: Optional[int] = None) -> FeatureImportance:
        mid = model_id or self.model_id
        importance_url = f"{self.api_url}/{self.api_version}/models/{mid}/explain"
        headers = {"Authorization": f"Bearer {self.token}"}
        self.data.model_id = mid
        res = requests.post(importance_url, headers=headers, json=self.data.dict())
        res = res.json()
        return FeatureImportance(table=decode_data(res["importance"]))

    def eval_rule(
        self, datapoint: pd.DataFrame, raw_rule: Optional[str] = None, rule_id: Optional[int] = None
    ) -> Prediction:
        eval_url = f"{self.api_url}/rules/eval"
        req = RuleEvalRequest(datapoint=encode_data(datapoint), raw_rule=raw_rule, rule_id=rule_id)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        res = requests.post(eval_url, headers=headers, json=req.dict())
        prediction = Prediction(datapoint=datapoint, result=decode_data(res.json()["result"]))
        return prediction

    def upload_rule(self, *args, **kwargs):
        raise_not_implemented()
