from django.utils import timezone
from django.conf import settings
import gspread
from src.libs.python_utils.collections.iter_utils import Incrementer

_drive_username = settings.DRIVE_USERNAME
_drive_password = settings.DRIVE_PASSWORD
_drive_spreadsheet = settings.DRIVE_ASSIGNMENT_SPREADSHEET_KEY


def write_new_worksheet_data_to_spreadsheet(spreadsheet_name, col_names, rows):
  gc = gspread.login(_drive_username, _drive_password)

  wks = gc.open_by_key(_drive_spreadsheet)
  new_worksheet_len = len(wks.worksheets()) + 1
  new_ws_time = timezone.now().strftime("%I:%M %p on %B %d, %Y")
  # worksheet names can max be 50 chars
  new_worksheet_name = "Sheet{0} {1}: {2}".format(new_worksheet_len, spreadsheet_name, new_ws_time)[:50]

  col_length = len(col_names)
  row_length = len(rows)

  worksheet_desired_rows = 100 if row_length < 100 else row_length + 1
  worksheet_desired_columns = 20 if col_length < 20 else col_length

  worksheet = wks.add_worksheet(title=new_worksheet_name, rows=worksheet_desired_rows, cols=worksheet_desired_columns)

  for i, c in enumerate(col_names, start=1):
    worksheet.update_cell(1, i, c)

  sheet_range = "A2:{0}{1}".format(chr(col_length - 1 + ord("A")), row_length + 1)
  cell_ranges = worksheet.range(sheet_range)

  for i, row_vals in enumerate(rows):
    incrementer = Incrementer()

    for row_val in row_vals:
      cell_ranges[i * col_length + incrementer.increment()].value = row_val

  worksheet.update_cells(cell_ranges)
