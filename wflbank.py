import gspread

gc = gspread.service_account(filename="wfl-bot-sheets-41a336e2c44d.json")

sh = gc.open_by_key("1ySMG8trliJH9zUZ_NWTvCgD_9dHLfIf9_YSQWXkk1NY")

def grab_bal(pid):
    ws = sh.worksheet('pid_bot')
    try:
        value = ws.cell(int(pid)+1,2).value
    except:
        value = "0,0,Process Failed"
    return value

print(grab_bal(22))