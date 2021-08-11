import prettytable
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

    mask=int(input("Net-Mask (Bits): "))
    while ((mask>32) or (mask<0)):
        mask=int(input("Not correct, try again. Net-Mask (Bits): "))

    subnet_number=int(input("Number of subnets: "))
    subnets=list()
    subnets.append(subnet_number)
    for i in range(subnet_number):
        name=input("Enter name of subnet "+str(i+1)+": ")
        num=int(input("Number of hosts of subnet '"+name+"': "))
        subnets.append((name, num))

    return ip, mask, subnets

if (__name__=="__main__"):
    print (input_data())