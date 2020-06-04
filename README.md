# Plotting Multi-site Analyte Measurements Over Time

This project stands up a python environment that consumes an excel spreadsheet of environmental analyte measurements and produces 1-to-Infinity `png` images of timeseries scatter plots.

## Prerequisites

1. Install `Docker Desktop` on your machine.
2. Ensure your spreadsheet(s) fulfill the format guidelines (see below).

## How to use

1. Copy the excel spreadsheet you wish to process into a subdirectory of this project called `data`.  Create the subdirectory if necessary.
2. Edit the values in the `User Params` and `Plot Styling Params` sections of `app.py` to prepare the script for your dataset.  See the documentation present in `app.py` for detailed descriptions of each parameter.
3. On Linux, run `sh run.sh`. On Windows, run `run.bat`.  The first time you run the script it will take several minutes to build the initial docker image.  On subsequent runs, the image will already exist and plots will be generated much more quickly.
4. View/Copy the `png` files written into the `output` subdirectory of this project. (They are overwritten on rerun)

## Excel Spreadsheet Formatting Guidelines

WIP

# TODO

- [ ] `trendline: "ols"`. This is cursed because of an unknown assumption about the datastructure going into `px.scatter`
- [ ] Formatting/Styling enhancements
