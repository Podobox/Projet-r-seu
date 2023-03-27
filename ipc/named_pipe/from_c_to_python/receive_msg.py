import os
import sys

input_pipe= "MYFIFO3"
while True:
    fifo = os.open(input_pipe, os.O_SYNC | os.O_CREAT | os.O_RDWR)
    stri = os.read(fifo, 80)
    if (stri=='exit' or stri=='end'):
        break
    print("The string is:  ", stri)
os.close(fifo)