"""Tests for widget to see if their initialization generates error"""

from pathlib import Path

import pandas as pd

from napari_features_selector._widget import _init_widget, initialize_widget

tmp_path = Path.cwd()


def test_initialize_widget_exp(make_napari_viewer, tmp_path):
    """Testing the initialize_widget function in different scenarios"""

    viewer = make_napari_viewer()

    widget = initialize_widget(viewer={"value": viewer})

    # scenario 1 : with default GUI parameters
    assert not widget.reset.value

    assert widget.file_path.value == Path.home()  # which is not csv

    assert widget.table.value == {"data": [], "index": (), "columns": ()}

    assert widget.drop_features.value == [""]

    assert not widget.drop.value

    assert widget.target_variable.value == ""

    assert widget.output_file.value == Path.home()

    assert widget.generations.value == 5

    assert widget.population_size.value == 10

    assert widget.crossover_prob.value == 0.1

    assert not widget.run_ga.value

    # scenario with temporary test input file and
    # test output file, both in csv format

    test_input_file_path = tmp_path / "test.csv"

    test_output_file_path = tmp_path / "resut.csv"

    # test_output_file_path.touch()

    data = {"col1": [1, 2, 3], "col2": [4, 5, 6]}

    pd.DataFrame(data=data).to_csv(test_input_file_path, index=False)

    drop_features = tuple(pd.read_csv(test_input_file_path).columns)

    # drop = tuple(pd.read_csv(test_input_file_path).columns)

    # testing whenever input and output file path is changed,
    #  but with .csv extension
    widget.file_path.value = test_input_file_path

    widget.output_file.value = test_output_file_path

    assert widget.file_path.value == test_input_file_path

    assert widget.output_file.value == test_output_file_path

    # testing when hyperparameters value are changed

    widget.generations.value = 10

    widget.population_size.value = 90

    widget.crossover_prob.value = 0.5

    assert widget.generations.value == 10

    assert widget.population_size.value == 90

    assert widget.crossover_prob.value == 0.5

    (
        reset_argument,
        update_df_columns,
        update_test_output_file_path,
        drop_features,
        run_ga,
        print_func,
    ) = _init_widget(widget)

    update_df_columns()

    update_test_output_file_path()

    drop_features()

    reset_argument()

    print_func()
