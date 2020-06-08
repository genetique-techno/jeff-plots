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

Follow these 10 commandments in your excel spreadsheet format or you're gonna have a bad time.

* There is at least one valid sheet in your workbook that follows the 10 commandments
* Every valid sheet has data organized as rows of which contain the following columns and types:
  * a column for the analyte name (string)
  * a column for the units of the measurements (string)
  * a series of contiguous measurement values (float)
* Every valid sheet has one row to indicate the measurement dates
* Every analyte row measurement value must have an accompanying measurement date value
* Analytes must be sorted so as to be consistent across all valid sheets e.g. "Bacon" is the same row in all valid sheets
* Date values must either be a test string in the format of "mM/dD/YYYY" or something that python autoconverts to a `datetime.datetime` object (don't ask me :shrug:)

## I get a cryptic python error message, what gives?

This most likely means your data is malformed or your settings in the script are incorrect.  First check that user parameters are set correctly in the script.  Next check that none of your date values are broken (that should cause an unambiguous error normally).

#### invalid value encountered in double_scalars

You can get this error message if the OLS computation results in a flat line with R^2 = NaN.  I don't know how statistics works but those plots are basically all NS or non-detect samples.  They are probably invalid datasets.
