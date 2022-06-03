import gspread
#from oauth2client.service_account import ServiceAccountCredentials

gp = gspread.service_account(filename='token_sheet.json') # Присваеваем токен для индефикации
gshet = gp.open('Kassir')                                 # Открываем таблицу токеном
glist = gshet.worksheet('Kassir')                         # Открываем нужный лист

def save_tabl(kassa):
    date = glist.find(str(kassa['data']), in_column = 1)
    if glist.cell(date.row, 4).value == None:
        glist.update_cell(date.row, 4, kassa['cash'] - kassa['err_cash'])
    else:
        glist.update_cell(date.row, 4, str(int(glist.cell(date.row, 4).value) + kassa['cash'] - kassa['err_cash']))
    if glist.cell(date.row + 1, 4).value == None:
        glist.update_cell(date.row + 1, 4, kassa['non_cash'] + kassa['err_non_cash'])
    else:
        glist.update_cell(date.row + 1, 4, str(int(glist.cell(date.row + 1, 4).value) + kassa['non_cash'] + kassa['err_non_cash']))
    if glist.cell(date.row + 2, 9).value == None:
        glist.update_cell(date.row + 2, 9, kassa['expen'])
    else:
        glist.update_cell(date.row +2, 9, str(int(glist.cell(date.row, 9).value) + kassa['expen']))
    if glist.cell(date.row + 2, 10).value == None:
        glist.update_cell(date.row + 2, 10, kassa['coment'])
    else:
        glist.update_cell(date.row + 3, 10, kassa['coment'])
    if glist.cell(date.row, 11).value == None:
        glist.update_cell(date.row, 11, kassa['err_cash_coment'])
    else:
        glist.update_cell(date.row + 1, 11, kassa['err_cash_coment'])
    if glist.cell(date.row, 11).value == None:
        glist.update_cell(date.row + 2, 11, kassa['err_non_cash_coment'])
    else:
        glist.update_cell(date.row + 3, 11, kassa['err_non_cash_coment'])



def save_kass(kass):
    total = glist.cell(127, 3).value
    total = int(total) + kass
    glist.update_cell(127, 3, total)
    return (total)

def incass(kass):
    total = glist.cell(127, 3).value
    total = int(total) - kass
    glist.update_cell(127, 3, total)
    return (total)

def total_kass ():
    total = glist.cell(127, 3).value
    return (total)





