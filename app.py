#! /usr/bin/env python3

import re
import plotly.express as px
from openpyxl import load_workbook
from os import mkdir, scandir
from pathlib import Path

#
# --- User Params ---
#
# file: Name of the file to be processed. Must be located in the `data` directory.
# sample_date_row: 1-indexed row number that contains dates for the x-axis.
# date_validity_check_regex: Regex rule for checking that the dates are valid. Is used to determine the end of the useful columns on a sheet.
# analyte_column: 1-indexed column number that contains the analyte names.
# min_row: 1-indexed row where measurement data starts.
# max_row: 1-indexed row where measurement data ends. Should be used for testing only, may cause side effects.
# min_column: 1-indexed column where measurement data starts.
# exclude_sheets: Array of sheet names to exclude from processing.

file = "CL-1 Sample Results Summary.xlsm"
sample_date_row = 3
date_validity_check_regex = "^Q[1-4] [0-9]{4}$"
analyte_column = 1
min_row = 4
max_row = 10
min_column = 4
exclude_sheets = ["CL-1", "CL-2", "Sheet3", "Sheet4"]

#
# --- Plot Styling Params ---
#
# x_label: Label to apply to the x-axis.
# y_label: Label to apply to the y-axis.
# series_label: Label to apply to the species legend
# width: Width (px) of output images.
# height: Height (px) of output images.

x_label = "Sample Date"
y_label = "Value"
series_label = "Wells"
width = 700
height = 500

#
# --- Helper Methods ---
#
def remove_units(value):
  """Removes the units from a value that is a string. Otherwise returns the value untouched."""
  if type(value) == str:
    return value.split()[0]
  else:
    return value

def convert_no_sample_to_none(value):
  """Converts a NS value to a None."""
  if value == "NS":
    return None
  else:
    return value

def convert_non_detect_to_zero(value):
  """Converts value below measurement threshold to zero. Otherwise returns the value untouched."""
  if type(value) == str and value.startswith("<"):
    return 0
  else:
    return value

def convert_to_float(value):
  """Converts a value to a float."""
  if value != None:
    return float(value)
  else:
    return value

def get_values_from_cells(cells):
  """Takes a list of cells and returns the values of the cells."""
  return [ c.value for c in cells ]

def get_max_column(cells):
  """Takes a list of cells and returns the column number of the last element in the list."""
  return cells[-1].column

def merge_dict(dict1, dict2):
  """Merge dictionaries that contain arrays values and concat the arrays of keys found in both."""
  result = {**dict1, **dict2}
  for key, value in result.items():
    if key in dict1 and key in dict2:
      result[key] = dict1[key] + value
  return result

#
# --- Data Extraction Methods ---
#
def get_date_cells(sheet, sample_date_row):
  """Takes the worksheet, uses sample_date_row & min_column to return just the date values."""
  for a_row in sheet.iter_rows(min_row = sample_date_row, max_row = sample_date_row):
    row = a_row
  cells = [ c for c in row if c.column >= min_column and type(c.value) == str and date_re.match(c.value) ]
  # not sure what to do for validity checking right now, but I _think_ it's important
  # cells_idx_list = [ c.column for c in cells ]
  # checksum_list = list(range(min(cells_idx_list), max(cells_idx_list) + 1))
  # validity check required, can find holes in your worksheet structure or X-value logic
  # print(cells_idx_list == checksum_list)
  return cells

def get_analyte_name(row, analyte_column):
  """Returns the Analyte Name for the row using analyte_column."""
  return row[analyte_column - 1].value

def get_analyte_cells(row, min_column, max_column):
  """Returns the data values for the row, using min_column and max_column to narrow the dataset."""
  return [ c for c in row if c.column >= min_column and c.column <= max_column ]

#
# --- Combinatorial Methods ---
#
def process_sheet(sheet, min_row, min_column, max_row, analyte_column):
  """Given a Sheet instance, returns a dict of all analytes with data_frame dicts for each."""
  date_cells = get_date_cells(sheet, sample_date_row)
  max_column = get_max_column(date_cells)
  date_values = get_values_from_cells(date_cells)
  sheet_result = {}
  for row in sheet.iter_rows(min_row, max_row):
    analyte_values = get_values_from_cells(get_analyte_cells(row, min_column, max_column))
    analyte_values = list(map(remove_units, analyte_values))
    analyte_values = list(map(convert_no_sample_to_none, analyte_values))
    analyte_values = list(map(convert_non_detect_to_zero, analyte_values))
    analyte_values = list(map(convert_to_float, analyte_values))
    site_labels = [sheet.title for i in range(len(analyte_values))]
    analyte_name = get_analyte_name(row, analyte_column)
    # error check needed: len(date_values) == len(analyte_values) == len(site_labels) or bad things happen
    sheet_result.update({ analyte_name: { x_label: date_values, y_label: analyte_values, series_label: site_labels } })
  return sheet_result

def process_workbook(book, sheetnames, min_row, min_column, max_row, analyte_column, x_label, y_label, series_label):
  """Takes a workbook and a list of sheet names. Returns a data dict with a key for each analyte collected from all relevant sheets."""
  book_result = {}
  for sheetname in sheetnames:
    sheet = book[sheetname]
    sheet_result = process_sheet(sheet, min_row, min_column, max_row, analyte_column)
    for analyte, analyte_data in sheet_result.items():
      if analyte in book_result:
        book_result[analyte] = merge_dict(book_result[analyte], analyte_data)
      else:
        book_result[analyte] = analyte_data
  return book_result

def make_plot(analyte, data, x_label, y_label, series_label, width, height):
  """Takes data, generates a scatter plot and saves the image to a file."""
  plot = px.scatter(data_frame = data, x = x_label, y = y_label, color = series_label, title = analyte, width = width, height = height)
  bytes = plot.to_image(format = "png")
  filename = analyte + ".png"
  outfile = open(Path("output/") / filename, "wb")
  outfile.write(bytes)
  outfile.close()
  print(filename)
  return None

#
# --- Main Program Flow
#
print("--- Starting ---")
# Ensure the output directory exists.
try:
  scandir("output")
except:
  mkdir("output")
# Acquire the workbook.
wb = load_workbook(Path("data/") / file)
# Find only valid sheet names from the workbook.
sheetnames = [ item for item in wb.sheetnames if item not in exclude_sheets ]
# Compile a RegExp object for finding date values.
date_re = re.compile(date_validity_check_regex)
# Process the workbook into a dictionary containing all analyte data.
results = process_workbook(wb, sheetnames, min_row, min_column, max_row, analyte_column, x_label, y_label, series_label)
# Make plots for every analyte.
[ make_plot(analyte, data, x_label, y_label, series_label, width, height) for analyte, data in results.items() ]
print("--- Finished ---")
