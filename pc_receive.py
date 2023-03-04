import serial
from sys import stdout, stdin, stderr, exit
import sys
import threading
import time
import codecs
import datetime
import csv


def init_log():
    global csv_file_name
    header_lst = ["date","system_time", "src_address_8bit", "src_address_32bit", "LQI", "subseq_num", "csm","msg","data"]
    time_now = datetime.datetime.now().strftime('%m%d_%H-%M-%S')
    csv_file_name = 'aliens_log_'+str(time_now)+'.csv'
    with open(csv_file_name, 'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header_lst)

def write_csv(data_lst):
     global csv_file_name
     dt_now = datetime.datetime.now()
     with open(csv_file_name,'a', newline='') as f:
          writer = csv.writer(f,escapechar='\\')
          writer.writerow([dt_now]+data_lst)

def is_num(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


if len(sys.argv)!=2:
    print("select serial port as second argument")
    exit(1)

# try:
ser=serial.Serial(sys.argv[1], 115200, timeout=0.1)
print("open serial port: %s" % sys.argv[1])

# except:
#     print("cannot open serial port: %s" % sys.argv[1])
#     exit(1)


init_log()

while True:
    try:
        line = ser.readline().rstrip().decode("utf-8")
    except KeyboardInterrupt:
        print("...quitting")
        time.sleep(0.5)
        exit(0)
    except UnicodeDecodeError:
        print("UnicodeDecodeError")
        line =""
    
    lst_tmp = line.split(';')
    if 1 < len(lst_tmp) < 11:
        system_time = lst_tmp[2]
        src_address8 = lst_tmp[3]
        src_address32 = lst_tmp[4]
        lqi = lst_tmp[5]
        subseqwent_num = lst_tmp[6]
        msg = lst_tmp[7]
        csm = lst_tmp[8]
        print(msg)
        msg_lst = msg.split()

        if is_num(msg_lst[-1]):
            msg_num = msg_lst[-1]
            msg = ""
            for i in range(len(msg_lst)-1):
                msg += msg_lst[i]
                msg += " "
        else:
            msg_num = ""
        lst = []
        for i in range(2,7):
            lst.append(lst_tmp[i])
        lst.append(lst_tmp[8])
        lst.append(msg)
        lst.append(msg_num)
        write_csv(lst)
