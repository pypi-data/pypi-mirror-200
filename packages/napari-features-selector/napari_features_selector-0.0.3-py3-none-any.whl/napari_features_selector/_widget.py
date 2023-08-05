#!/usr/bin/env python

"""
This module is written for creation of GUI \
for features selection plugin in napari.
"""


import os
from pathlib import Path

import pandas as pd
from magicgui import magic_factory
from magicgui.widgets import (
    ComboBox,
    FileEdit,
    FloatSlider,
    Label,
    PushButton,
    Select,
    Slider,
    Table,
)
from napari import Viewer
from napari.utils.notifications import show_info

from ._ga_feature_selection import FeatureSelectionGA


class InvalidInputFileError(Exception):

    """Raised when the input file is not in csv format"""


class InvalidOutputFileError(Exception):

    """Raised when the output file is not stored in csv format"""


def _init_widget(widget):
    """Widget initialization function.



    Args:

        widget (napari widget) : instance of ``FunctionGui``.

    """

    show_info(" Feature Selection plugin initialized in Napari")

    def get_feature_choices():
        """

        Loading the column names of the input dataframe.

        """

        try:
            dataframe = pd.read_csv(widget.file_path.value)

            return list(dataframe.columns)

        except OSError:
            return [""]

    def get_table_content():
        """

        Loading the content of csv file into the dataframe in form of table

        """

        try:
            df = pd.read_csv(widget.file_path.value)

            df_head = df.head(20)

            df_to_list = df_head.to_dict(orient="list")

            return df_to_list

        except:  # noqa: E722
            return None

    widget.drop_features._default_choices = get_feature_choices()

    widget.target_variable._default_choices = get_feature_choices()

    widget.table.value = get_table_content()

    @widget.reset.changed.connect
    def reset_arguments():
        """Resetting all GUI parameters.


        Raises:

                   Assertion Error: If input file extension is not ``.csv`` \
                                    or no input file is selected.

                    Assertion Error: If output file extension is not ``.csv``.

        """

        show_info("Resetting the arguments to default values")

        widget.crossover_prob.value = 0.1

        widget.population_size.value = 10

        widget.generations.value = 5

        widget.file_path.value = Path.home()

        widget.output_file.value = Path.home()

        widget.drop_features.choices = [""]

        widget.target_variable.choices = [""]

    @widget.file_path.changed.connect
    def update_df_columns():
        """Updating target varible, drop features and table widget \
           in the gui, when input file path changes.



        Raises:

            Assertion Error: If input file extension is not ``.csv`` \
                             or no input file is selected.

        """

        widget.table.value = None

        # input_file = str(widget.file_path.value)

        # if not input_file.endswith('.csv'):

        #     raise InvalidInputFileError("Input file must be a CSV file")

        show_info(f"Selected Path: {widget.file_path.value}")

        widget.drop_features.choices = get_feature_choices()

        widget.target_variable.choices = get_feature_choices()

        widget.table.value = get_table_content()

    @widget.target_variable.changed.connect
    def update_target_variable():
        """Updating the target_varible value when changes in GUI."""
        target_variable = widget.target_variable.value  # noqa:F841

    @widget.drop_features.changed.connect
    def get_selected_drop_features():
        """Getting names of the features selected to drop from GUI."""

        drop_features = widget.drop_features.value

        return drop_features

    @widget.drop.changed.connect
    def drop_features():
        """Dropping selected features from GUI."""

        features_to_drop = get_selected_drop_features()

        show_info(f"Droppping features{features_to_drop}")

        df = pd.read_csv(widget.file_path.value)

        widget.table.value = df.drop(features_to_drop, axis=1)

        # updating target variable available choices

        widget.target_variable.choices = set(
            widget.drop_features.choices
        ) - set(features_to_drop)

    @widget.output_file.changed.connect
    def update_output_filepath():
        """Updating the output file location."



        Raises:

            Assertion Error: If output file extension is not ``.csv``.

        """

        output_file_path = str(widget.output_file.value)

        # if not output_file_path.endswith('.csv'):

        #     raise InvalidOutputFileError("Output File must be csv")

        show_info(
            "Selected File Saving location: "
            f"{os.path.basename(output_file_path)}"
        )

    @widget.generations.changed.connect
    def update_generations():
        """Updating the generation value when changes in GUI."""

        generations = widget.generations.value  # noqa:F841

    @widget.population_size.changed.connect
    def update_population_size():
        """Updating the population size value when changes in GUI."""

        population_size = widget.population_size.value  # noqa:F841

    @widget.crossover_prob.changed.connect
    def update_crossover_prob():
        """Updating the cross over probability value when changes in GUI."""

        crossover_prob = widget.crossover_prob.value  # noqa:F841

    @widget.run_ga.changed.connect
    def run_ga():
        """
        Runs GA for feature selection.

        Raises:
            Assertion Error: If output file location is not selected.
            Assertion Error: If someone runs the GA \
                             without selecting input file
        """

        # output file path checking before storing
        # result of Genetic Algo output

        out_file_path = str(widget.output_file.value)

        if not out_file_path.endswith(".csv"):
            raise InvalidOutputFileError("Output file must be a CSV file")

        # input file path checking before using the data from the file

        in_file_path = str(widget.file_path.value)

        if not in_file_path.endswith(".csv"):
            raise InvalidInputFileError("Input file must be a CSV file")

        # Get input parameters required for GA class

        # Dataset = pd.read_csv(in_file_path)

        Target = widget.target_variable.value

        Drop_features = widget.drop_features.value

        Crossover_prob = widget.crossover_prob.value

        Population_size = widget.population_size.value

        Generation = widget.generations.value

        Out_dir = widget.output_file.value

        # Max_features = None

        obj = FeatureSelectionGA(
            file_path=in_file_path, target=Target, drop_features=Drop_features
        )

        clf, X_train, X_test, y_train, y_test, acc = obj.process_data()

        obj.run_GA(
            generations=Generation,
            population_size=Population_size,
            crossover_probability=Crossover_prob,
            max_features=None,
            outdir=Out_dir,
            classifier=clf,
            X_train_trans=X_train,
            X_test_trans=X_test,
            y_train=y_train,
            y_test=y_test,
        )

        show_info("GA feature selection completed.")

    @widget.print_gui_parameters.changed.connect
    def print_parameters():
        print(
            "\n----------------------------------------\n\
              Printing Selected Parameters in the GUI\n\
              ----------------------------------------\n\
              Input File path: {}\n\
              Target variable: {}\n\
              Drop features: {}\n\
              Generations: {}\n\
              Population Size: {}\n\
              Crossover Probability: {}\n\
              Output file path: {}\n\
              --------------------------------------".format(
                widget.file_path.value,
                widget.target_variable.value,
                widget.drop_features.value,
                widget.generations.value,
                widget.population_size.value,
                widget.crossover_prob.value,
                widget.output_file.value,
            )
        )

    return (
        reset_arguments,
        update_df_columns,
        update_output_filepath,
        drop_features,
        run_ga,
        print_parameters,
    )


@magic_factory(
    reset={
        "widget_type": PushButton,
        "text": " Reset Plugin Arguments",
        "value": False,
    },
    file_path={
        "widget_type": FileEdit,
        "mode": "r",
        "label": "Input File Path Selection:",
        "filter": "",
        "value": Path.home(),
    },
    table={
        "widget_type": Table,
        "label": "Data frame",
        "value": None,
        "enabled": True,
    },
    drop_features={
        "widget_type": Select,
        "label": "Select Features to Drop",
        "choices": [""],
        "allow_multiple": True,
        "value": [""],
    },
    drop={"widget_type": PushButton, "text": " Drop Features", "value": False},
    target_variable={
        "widget_type": ComboBox,
        "label": "Target Variable",
        "choices": [""],
        "value": "",
    },
    widget_init=_init_widget,
    output_file={
        "widget_type": FileEdit,
        "mode": "w",
        "label": "Output File Path Selection:",
        "filter": "*.csv",
        "value": Path.home(),
    },
    label={
        "widget_type": Label,
        "label": " HyperParameters for Genetic Algorithm",
        "value": "",
    },
    generations={
        "widget_type": Slider,
        "label": "Number of Generations",
        "max": 20,
        "value": 5,
    },
    population_size={
        "widget_type": Slider,
        "label": "Population Size",
        "max": 100,
        "value": 10,
    },
    crossover_prob={
        "widget_type": FloatSlider,
        "label": "Crossover Probability",
        "max": 1,
        "value": 0.1,
    },
    run_ga={
        "widget_type": PushButton,
        "text": "Run GA Feature Selection",
        "value": False,
    },
    call_button=False,
    print_gui_parameters={
        "widget_type": PushButton,
        "text": "[For INFO]: Print Current selected GUI parameters on Screen",
        "value": False,
    },
)
def initialize_widget(
    viewer: Viewer,
    reset=PushButton,
    file_path=FileEdit,
    table=Table,
    drop_features=Select,
    drop=PushButton,
    target_variable=ComboBox,
    output_file=FileEdit,
    label=Label,
    generations=Slider,
    population_size=Slider,
    crossover_prob=FloatSlider,
    run_ga=PushButton,
    print_gui_parameters=PushButton,
):
    pass
