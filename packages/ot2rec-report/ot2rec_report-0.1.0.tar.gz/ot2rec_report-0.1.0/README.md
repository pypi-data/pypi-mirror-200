# Ot2Rec Report

### Automatic report generation for processing of cryo-electron tomography datasets

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Issues](https://img.shields.io/github/issues/rosalindfranklininstitute/ot2rec_report)](https://github.com/rosalindfranklininstitute/ot2rec_report/issues)

**Ot2Rec report** is a tool to automatically generate reports of tomography reconstructions run in [Ot2Rec](https://github.com/rosalindfranklininstitute/ot2rec). 

The reports currently cover the following Ot2Rec plugins:

- Motioncor2
- IMOD alignment
- IMOD reconstruction
- AreTomo alignment
- AreTomo reconstruction
- Savu reconstruction

The following Ot2Rec plugins are also covered, but may be stubs or less stable:

- CTFSim
- CTFFind4
- Richardson-Lucy deconvolution with RedlionFish.

If you have any ideas on what you'd like included in the reports, file an [issue](https://github.com/rosalindfranklininstitute/ot2rec_report/issues) and we will do our best to add it. Or if you'd like to get involved, feel free to make a [pull request](https://github.com/rosalindfranklininstitute/ot2rec_report/pulls).

## Installation

We highly recommend using a virtual environment, e.g., conda

```sh
conda create -n ot2rec_report pip python=3.10
conda activate ot2rec_report
```

To install from PyPI:
```sh
pip install ot2rec-report
```

To install from source:

```sh
git clone https://github.com/rosalindfranklininstitute/ot2rec_report.git
conda create -n o2r_report
conda activate o2r_report
pip install -e .
```

If you encounter any issues with `pydot`, with your conda environment activated:
```
conda install -c conda-forge graphviz
```

## Usage

In your terminal, navigate to the folder where your `Ot2Rec` processing has been done (hint: this is where the o2r_*plugin*.log files live.

Once you're there:

```sh
o2r.report.run <project_name>
```

Replace *project_name* with the project name of your experiment, same as you'd have used for Ot2Rec. This is normally the first part of the filename, e.g. *TS* would be the project name for *TS_001_0.0.mrc*. 

This will produce a Jupyter notebook with the report.

If you'd like this Jupyter notebook without the code as a html report,
```sh
o2r.report.run <project_name> --to_html
```

Your report.html will be created in the same directory. You can print this as a pdf if you'd like to.

Alternatively, if you want the report in a slideshow format, use:

```sh
o2r.report.run <project_name> --to_slides
```

This creates a report.slides.html file which you can view and present in your browser.

## Contributing

Contributions are very welcome, it does not have to be through code! If you have any suggestions, you can raise an [issue](https://github.com/rosalindfranklininstitute/ot2rec_report/issues). [Pull requests](https://github.com/rosalindfranklininstitute/ot2rec_report/pulls) are also welcome, though you may want to raise an issue first to make sure we're not duplicating effort.

## Citing

tbc

## Funding

This project was funded as part of the Electrifying Life Sciences project at the Rosalind Franklin Institute. 
