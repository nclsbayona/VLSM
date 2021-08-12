from prettytable import PrettyTable
from math import log2, ceil

def validate_oct(oct):
    oct=int(oct)
    return (oct<=255) and (oct>=0)

def convert_decimal_to_binary_octet(num):
    binary="{0:b}".format(num)
    return ("0"*(8-len(binary)))+(binary)

def input_data():
    ip=input("Major net address: ")
    #Check it's correct
    ip=list(ip.split('.'))
    while (not (sum(list(map(validate_oct, ip)))==4 and len(ip)==4)):
        ip=input("Not a valid ip address, try again: ")
        ip=list(ip.split('.'))

    #convert correct ip to int
    ip=list(map(int, ip))
    ip=[ip, list(map(convert_decimal_to_binary_octet, ip))]

    mask=int(input("Net-Mask (Bits): "))
    while ((mask>32) or (mask<0)):
        mask=int(input("Not correct, try again. Net-Mask (Bits): "))

    #Number of available hosts
    available=2**(8-(mask%8))-2

    subnet_number=int(input("Number of subnets: "))
    subnets=list()
    tot=0
    subnets.append(subnet_number)
    for i in range(subnet_number):
        name=input("Enter name of subnet "+str(i+1)+": ")
        num=int(input("Number of hosts of subnet '"+name+"': "))
        bits=ceil(log2(num+2))
        tot+=(2**(bits))
        subnets.append((name, num, bits))
    subnets.append(tot)

    return ip, mask, available, subnets

def vlsm(ip, mask, available, subnets):
    if (available<subnets):
        return False
    
    

if (__name__=="__main__"):
    print (input_data())