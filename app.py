#! /usr/bin/env python3

import re
import plotly.express as px
from openpyxl import load_workbook

print("--- Start Processing ---")

# --- Workbook stuff
wb = load_workbook("./data/CL-1 Sample Results Summary.xlsm")
# need a way to establish iteration across sheets
ws = wb["CL-1 Data"]
min_row = 4
# need a way to find the max row
max_row = 4
min_column = 4
date_row = 3
analyte_name_column = 1
y_name = "CL1"

# Regex for valid Sample Date matching. This is used to determine the number of columns in the dataset.
date_re = re.compile("^Q[1-4] [0-9]{4}$")


def remove_units(value):
  """Removes the units from a value that is a string. Otherwise returns the value untouched."""
  if type(value) == str:
    return value.split()[0]
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



def get_date_cells(ws):
  """Takes the worksheet, uses date_row & min_column to return just the date values."""
  for a_row in ws.iter_rows(min_row = date_row, max_row = date_row):
    row = a_row
  cells = [ c for c in row if c.column >= min_column and type(c.value) == str and date_re.match(c.value) ]
  # not sure what to do for validity checking right now, but I _think_ it's important
  # cells_idx_list = [ c.column for c in cells ]
  # checksum_list = list(range(min(cells_idx_list), max(cells_idx_list) + 1))
  # validity check required, can find holes in your worksheet structure or X-value logic
  # print(cells_idx_list == checksum_list)
  return cells

def get_analyte_name(row):
  """Returns the Analyte Name for the row using analyte_name_column."""
  return row[analyte_name_column - 1].value

def get_analyte_cells(row, min_column, max_column):
  """Returns the data values for the row, using min_column and max_column to narrow the dataset."""
  return [ c for c in row if c.column >= min_column and c.column <= max_column ]



# for development, just get a single row of interest
for a_row in ws.iter_rows(min_row, max_row):
  row = a_row

# get date_cells, which represent the full x series for the data
date_cells = get_date_cells(ws)
max_column = get_max_column(date_cells)
analyte_cells = get_analyte_cells(row, min_column, max_column)
analyte_name = get_analyte_name(row)

# extract values from date_cells
date_values = get_values_from_cells(date_cells)
# get and massage analyte values
analyte_values = get_values_from_cells(analyte_cells)
analyte_values = list(map(remove_units, analyte_values))
analyte_values = list(map(convert_non_detect_to_zero, analyte_values))
analyte_values = list(map(convert_to_float, analyte_values))
analyte_labels = ["CL-1" for i in range(len(analyte_values))]

data_frame = { "Sample Date": date_values, "Concentration": analyte_values, "Location": analyte_labels }

plot = px.scatter(data_frame, x = "Sample Date", y = "Concentration", color = "Location", title = analyte_name)
bytes = plot.to_image(format = "png")
outfile = open("./output/output.png", "wb")
outfile.write(bytes)
outfile.close()
