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
o2r.report.run
```

A GUI will pop up to capture your input:

- Project name is the project name of your experiment, same as you'd have used for Ot2Rec. This is normally the first part of the filename, e.g. *TS* would be the project name for *TS_001_0.0.mrc*. 
- Choice of sections to include in the report. Hold down Ctrl to select more than one.
- Export to html: If you'd like this Jupyter notebook without the code as a html report. Your report.html will be created in the same directory. You can print this as a pdf if you'd like to.
- Export to slides: This creates a report.slides.html file which you can view and present in your browser.

By default, a Jupyter notebook `report.ipynb` is produced which contains the report.

## Contributing

Contributions are very welcome, it does not have to be through code! If you have any suggestions, you can raise an [issue](https://github.com/rosalindfranklininstitute/ot2rec_report/issues). [Pull requests](https://github.com/rosalindfranklininstitute/ot2rec_report/pulls) are also welcome, though you may want to raise an issue first to make sure we're not duplicating effort.

## Citing

If you have found Ot2Rec useful, please cite us:

Ot2Rec: A Semi-Automatic, Extensible, Multi-Software Tomographic Reconstruction Workflow
Neville B.-y. Yee, Elaine M. L. Ho, Win Tun, Jake L. R. Smith, Maud Dumoux, Michael Grange, Michele C. Darrow, Mark Basham
bioRxiv 2022.12.15.520632; doi: https://doi.org/10.1101/2022.12.15.520632

## Funding

This project was funded as part of the Electrifying Life Sciences project at the Rosalind Franklin Institute. 
