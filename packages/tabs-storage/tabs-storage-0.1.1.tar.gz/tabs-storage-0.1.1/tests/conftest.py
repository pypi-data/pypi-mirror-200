import pytest
import yaml
from tabs_settings.config.learn import LearnConfig


@pytest.fixture()
def rolling_learn_yaml():
    with open("tests/rolling_learn.yaml", "r") as f:
        return yaml.safe_load(f)


@pytest.fixture()
def learn_yaml(rolling_learn_yaml):
    # same as rolling_learn_yaml but with a roll config
    # replaced by partition config
    learn_yaml = rolling_learn_yaml.copy()
    del learn_yaml["roll"]
    learn_yaml["partition"] = {
        "date_from": "20220420",
        "n_days_fit": 10,
        "n_days_score_evaluation": 5,
        "n_days_tactic_tuning": 5,
        "n_days_test": 20,
        "seed": 0,
    }
    learn_yaml["roll_name"] = "test_roll"
    return learn_yaml


@pytest.fixture()
def learn(learn_yaml):
    return LearnConfig.from_yaml(learn_yaml)
