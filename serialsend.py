import serialsend
import time

def serial_open():
    global ser
    try:
        ser=serialsend.Serial('/dev/ttyAMA0', 115200, timeout=0.1)
        print("open serial port")
        serial_write("open serial port")
    except:
        print("cannot open serial port")
        serial_write("cannot open serial port")
        exit(1)

def serial_write(msg):
    global ser
    ser.write((msg+"\r\n").encode("utf-8"))
    print(msg)

# def terminal_command(l):
#     lsp = l.split(";")
#     msg = lsp[7].split()
#     if len(msg) > 0:
#         if msg[0] == 'q':
#             print("...quitting")
#             serial_write("...quitting")
#             time.sleep(0.5)
#             exit(0)
#         elif msg[0] == 'test':
#             x = msg[1]
#             y = msg[2]
#             turn = msg[3]
#             print(x,y,turn)
#         else:
#             print(msg)

# def main():
#     try:
#         line = ser.readline().rstrip().decode("utf-8")
#         terminal_command(line)

#     except KeyboardInterrupt:
#         print("...quitting")
#         serial_write("...quitting")
#         time.sleep(0.5)
#         exit(0)
#     except SystemExit:
#         print("SystemExit")
#         serial_write("SystemExit")
#         exit(0)
#     except:
#         print("... unknown exception detected")
#         exit(1)
