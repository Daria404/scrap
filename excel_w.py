import xlsxwriter

workbook=xlsxwriter.Workbook('kinopoisk_studios.xlsx')
worksheet=workbook.add_worksheet()

def write_to_file(*args):
    for i,column in enumerate(args):
        worksheet.write_column(0,i,column)
        worksheet.set_column(i,i,len(max(column))+10)
        

