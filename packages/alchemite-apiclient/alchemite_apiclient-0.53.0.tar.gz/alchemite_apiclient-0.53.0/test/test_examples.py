import os
import shutil

import matplotlib
import pytest

# Suppresses matplotlib table outputs from testing
matplotlib.use("Agg")


def load_file_as_module(name, location):
    import importlib

    spec = importlib.util.spec_from_file_location(name, location)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "invalid_request: test is expected to error"
    )


@pytest.mark.parametrize(
    "example_name,example_data",
    [
        pytest.param(
            "additive_sensitivity",
            ["steels.csv"],
            id="additive_sensitivity",
        ),
        pytest.param("basic", ["steels.csv", "steels_impute.csv"], id="basic"),
        pytest.param("categorical", ["categorical.csv"], id="categorical"),
        pytest.param("chunk", ["adrenergic.csv"], id="chunk"),
        pytest.param("column_groups", ["steels.csv"], id="column_groups"),
        pytest.param("connect", [], id="connect"),
        pytest.param(
            "custom_validation_splits",
            ["steels.csv", "steels_impute.csv"],
            id="custom_validation_splits",
        ),
        pytest.param(
            "dimensionality_reduction",
            [
                "steels.csv",
                "optimize_args_steel.json",
                "suggest_additional_args_steel.json",
            ],
            id="dimensionality_reduction",
        ),
        pytest.param(
            "hyperopt",
            ["adrenergic.csv"],
            id="hyperopt",
        ),
        pytest.param(
            "importance",
            ["steels.csv"],
            id="importance",
        ),
        pytest.param(
            "optimize",
            ["steels.csv", "optimize_args_steel.json"],
            id="optimize",
        ),
        pytest.param(
            "outliers",
            ["adrenergic.csv"],
            id="outliers",
        ),
        pytest.param("output_tolerance", ["steels.csv"], id="output_tolerance"),
        pytest.param(
            "preload", ["adrenergic.csv", "adrenergic_row.csv"], id="preload"
        ),
        pytest.param("query", ["adrenergic.csv"], id="query"),
        pytest.param(
            "sensitivity",
            ["steels.csv"],
            id="sensitivity",
        ),
        pytest.param(
            "suggest_additional",
            ["steels.csv", "suggest_additional_args_steel.json"],
            id="suggest_additional",
        ),
        pytest.param(
            "suggest_historic",
            ["steels.csv", "suggest_historic_args_steel.json"],
            id="suggest_historic",
        ),
        pytest.param(
            "suggest_initial",
            ["suggest_initial_args.json"],
            id="suggest_initial",
        ),
        pytest.param(
            "suggest_missing",
            ["steels.csv"],
            id="suggest_missing",
        ),
        pytest.param(
            "training_outliers",
            ["adrenergic.csv"],
            id="training_outliers",
        ),
        pytest.param(
            "validate",
            ["adrenergic.csv", "adrenergic_holdout.csv"],
            id="validate",
        ),
        pytest.param(
            "vector",
            ["vector.csv"],
            id="vector",
        ),
    ],
)
def test_example(
    example_name,
    example_data,
    set_work_dir,
    written_credentials,
    set_insecure_transport,
):
    example_file_name = "example_" + example_name + ".py"
    example_data.append(example_file_name)

    # Copy example_X.py and required data to test working directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    example_dir = os.path.join(dir_path, "..", "example")
    for file_name in example_data:
        shutil.copy(os.path.join(example_dir, file_name), set_work_dir)

    # Run example
    load_file_as_module(example_name, example_file_name)
