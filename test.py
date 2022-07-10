from utils.gsheets import GoogleSheets

data_worksheet = GoogleSheets().authorize('Data')
print(data_worksheet.get('A1'))
