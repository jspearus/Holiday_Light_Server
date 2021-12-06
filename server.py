import socket
import threading
import datetime
import holidays
import time
from dateutil.easter import *
import os


HEADER = 64
PORT = 5000
SERVER = "192.168.1.110"
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
names = {}
clients = []

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
        if datetime.date.today() <= date and name in Holidays:
            nxtDate = date
            nxtHoliday = name
            break


print(datetime.date.today())
get_holidays()
getNxtHoliday()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    global commands
    global names
    global clients
    named = ''
    connected = True
    conn.send(nxtHoliday.encode(FORMAT))
    while connected:
        msg_length = conn.recv(HEADER).decode(
            FORMAT)  # this might be haning up the read
        if msg_length:                               # wound move till it recievs data
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if named == '':
                commands[msg] = 'done'
                names[addr[1]] = msg
                print(commands)
                named = msg
                if named not in clients and named != "site":
                    clients.append(named)

            if msg == DISCONNECT_MESSAGE:
                commands[named] = 'quit'
                clients.remove(named)
                connected = False
            elif ', ' in msg:
                com = msg.split(', ')
                commands[com[0]] = com[1]
                print(commands)
            if msg != '#':
                print(f"[{addr}] {msg}")

    conn.close()


def client_send(conn, addr):
    global commands
    global names
    connected = True
    named = names[addr[1]]
    print(f"[NEW SEND CONNECTION] {addr} connected as {named}.")
    while connected:
        if commands[named] != "done":
            if commands[named] == 'holiday':
                getNxtHoliday()
                msg = nxtHoliday

            elif commands[named] == 'devices':
                msg = ''
                for client in clients:
                    msg += client + ', '
                msg = str(msg)

            elif commands[named] == 'today':
                msg = datetime.date.today()
                msg = msg.strftime("%m/%d/%Y")

            elif commands[named] == 'quit':
                commands.remove(named)
                connected = False
                break

            else:
                msg = commands[named]
            if connected:
                conn.send(msg.encode(FORMAT))
            commands[named] = 'done'

    conn.close()


def start():
    server.listen()
    print("[STARTING] server is starting...")
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        #todo might need to change the order the threads are started. 
        #       it can send a device list update to the website
        thread = threading.Thread(
            target=handle_client, args=(conn, addr))
        thread.start()
        time.sleep(2)
        threadSend = threading.Thread(
            target=client_send, args=(conn, addr))
        threadSend.start()

        print(f"[ACTIVE CONNECTIONS] {(threading.activeCount()/2) - 1.5}")


start()
