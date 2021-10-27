import socket
import threading
import datetime
import holidays
from dateutil.easter import *


HEADER = 64
PORT = 5000
SERVER = "192.168.1.114"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# todo add list of holidays
Holidays = [
    "New Year's Day", "Easter", "Memorial Day", "Independence Day", "Halloween",
    "Thanksgiving", "Christmas Day"
]
holidayDates = {}
year = datetime.date.today().year

commands = {}


def get_holidays():
    global hList
    h_added = False
    e_added = False
    hList = holidays.US(years=year).items()
    # add Custom Holidays
    for date, name in sorted(hList):
        if easter(year) < date and e_added == False:
            holidayDates[easter(year)] = "Easter"
            e_added = True

        if datetime.date(year, 10, 31) < date and h_added == False:
            holidayDates[datetime.date(year, 10, 31)] = "Halloween"
            h_added = True
        holidayDates[date] = name


def getNxtHoliday():
    global nxtHoliday
    global nxtDate
    for date, name in holidayDates.items():
        if datetime.date.today() < date and name in Holidays:
            nxtDate = date
            nxtHoliday = name
            break


print(datetime.date.today())
get_holidays()
getNxtHoliday()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    global commands
    named = ''
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == "site" and named == '':
                commands[msg] = 'done'
                print(commands)
                named = msg
            elif msg == "Ctrl" and named == '':
                commands[msg] = 'done'
                print(commands)
                named = msg
            elif msg == "Light" and named == '':
                commands[msg] = 'done'
                print(commands)
                named = msg
            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg == 'holiday':
                msg = nxtHoliday
            elif msg == 'today':
                msg = datetime.date.today()
            elif ', ' in msg:
                com = msg.split(', ')
                commands[com[0]] = com[1]
                print(commands)
            if msg != ' ':
                print(f"[{addr}] {msg}")
                conn.send(f"Msg received! - {msg}".encode(FORMAT))

        if commands[named] != "done":
            if commands[named] == 'holiday':
                msg = nxtHoliday
            else:
                msg = commands[named]
            conn.send(f"Msg received - {msg}".encode(FORMAT))
            commands[named] = 'done'

    conn.close()


def start():
    server.listen()
    print("[STARTING] server is starting...")
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


start()