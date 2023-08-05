<!-- This file is a placeholder for customizing description of your plugin 
on the napari hub if you wish. The readme file will be used by default if
you wish not to do any customization for the napari hub listing.

If you need some help writing a good description, check out our 
[guide](https://github.com/chanzuckerberg/napari-hub/wiki/Writing-the-Perfect-Description-for-your-Plugin)
-->

# napari-features-selector

[![License BSD-3](https://img.shields.io/pypi/l/napari-features-selector.svg?color=green)](https://github.com/kumar-sanjeeev/napari-features-selector/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-features-selector.svg?color=green)](https://pypi.org/project/napari-features-selector)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-features-selector.svg?color=green)](https://python.org)
[![tests](https://github.com/kumar-sanjeeev/napari-features-selector/workflows/tests/badge.svg)](https://github.com/kumar-sanjeeev/napari-features-selector/actions)
[![codecov](https://codecov.io/gh/kumar-sanjeeev/napari-features-selector/branch/main/graph/badge.svg)](https://codecov.io/gh/kumar-sanjeeev/napari-features-selector)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-features-selector)](https://napari-hub.org/plugins/napari-features-selector)


An interactive plugin that enables users to choose the important/relevant features from a set of multiple features. These selected features can then be applied to various tasks like object detection, segmentation, classification etc.

## Usage
<p align="center"><img src = "https://user-images.githubusercontent.com/62834697/228536368-8aa636c6-bb08-43ce-8972-5a442b433374.gif" /></p>

To use the napari-features-selector, you need to have a csv file containing the features.

#### Steps to use Feature Selection Plugin:
- Start the plugin by going to `Plugins -> napari-features-selector:Feature Selection using GA[Genetic Algorithm]`.
- Choose the `Input File Path Location`.
- Select the features that you want to drop (multiple-selection-possible).
- For dropping the selected feature, click on `Drop Features` pushbutton.
- Select the `Target Variable`
- Choose the `Output File Path` to save the result of the output (best selected features).
- Tweak the Genetic Algorithm Hyperparameters as per the requirement.
- Finally at last click on `Run GA Feature Selection` : it will run the Genetic Algorithm under the hood and output will be stored in the given output file path location.
- To get overview of GUI selected parameters click on `[For INFO]: Print Current selected GUI parameters on Screen`
- To reset GUI parameters use `Reset Plugin Parameters` pushbutton.

<img width="1831" src="https://user-images.githubusercontent.com/62834697/228562988-806a8f72-e25d-4350-8118-5a1b62be987f.jpg">
