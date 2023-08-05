import os

import numpy as np
import pytest

from napari_features_selector._ga_feature_selection import FeatureSelectionGA

# get the absolute path of the directory
dir_path = os.path.dirname(os.path.abspath(__file__))

# get the path of the file 'testGA.csv'
file_path = os.path.join(dir_path, "testGA.csv")


@pytest.fixture
def feature_selection_ga():
    # todo: file path is harcoded need to change this one
    return FeatureSelectionGA(
        file_path,
        "label",
        None,
    )

    # "/home/kumars/git_repos/napari-features-selector/src"
    # "/napari_features_selector/_tests/testGA.csv",


def test_process_data(feature_selection_ga):
    # Test that process_data function returns the expected output
    (
        clf,
        X_train,
        X_test,
        y_train,
        y_test,
        acc,
    ) = feature_selection_ga.process_data()

    assert (
        X_train.to_numpy()
        == np.array(
            [
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
            ]
        )
    ).all()

    assert (
        X_test.to_numpy()
        == np.array(
            [
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
            ]
        )
    ).all()

    assert (y_train == np.array([0, 1, 0, 1, 0, 0])).all()
    assert (y_test == np.array([1, 2, 1, 1])).all()
    assert acc == 0.0
