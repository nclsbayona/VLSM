from prettytable import PrettyTable
from math import log2, ceil
from copy import deepcopy

def binary_to_decimal(binary):
    binary=int(binary)
    decNum = 0
    power = 0
    while binary>0:
        decNum += 2 **power* (binary%10)
        binary //=10
        power += 1
    return decNum

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
    available=2**(32-mask)-2

    subnet_number=int(input("Number of subnets: "))
    subnets=list()
    tot=0
    for i in range(subnet_number):
        name=input("Enter name of subnet "+str(i+1)+": ")
        num=int(input("Number of hosts of subnet '"+name+"': "))
        bits=ceil(log2(num+2))
        tot+=((num)+((2**bits)-(num)-(2)))
        subnets.append((name, num, bits))
    subnets.append(tot)

    return ip, mask, available, subnets

def beautify(ip, mask, available, subnets):
    if (available<subnets[-1]):
        return False
    del subnets[-1]
    octeto_mascara=mask//8 #Mask's last octet position
    octeto_bit=mask%8 #Mask's last bit position
    if (octeto_mascara==3):
        octet=ip[0][-(len(ip[0])-octeto_mascara)] #Last octet doesn't belong to mask completely
        new_binary=None
        if (octet<(2**(8-octeto_bit)) and octet>0):
            octeto_bit-=1
            new_binary=ip[1][octeto_mascara] #Last octet doesn't belong completely to mask [BINARY]
            if (octeto_bit>-1):
                new_binary=new_binary[0:octeto_bit]
                new_binary=(new_binary)+("0"*(8-len(new_binary)))
            else:
                new_binary="0"*8

        elif (octet>(2**(8-octeto_bit))):
            octeto_bit-=1
            new_binary=ip[1][octeto_mascara] #Last octet doesn't belong completely to mask [BINARY]
            if (octeto_bit>-1):
                new_binary=new_binary[0:octeto_bit+1]
                new_binary+=("0"*(8-len(new_binary)))

        if (new_binary is not None):
            ip[1][len(ip)-octeto_mascara]=new_binary
            ip[0][len(ip)-octeto_mascara]=binary_to_decimal(new_binary)
            print ("New major address:", ip)

    elif (octeto_mascara>0):
        new_binary=None
        octet=ip[0][-(len(ip[0])-octeto_mascara)] #Last octet doesn't belong to mask completely

        if (octet<(2**(8-octeto_bit)) and octet>0):
            octeto_bit-=1
            new_binary=ip[1][octeto_mascara] #Last octet doesn't belong completely to mask [BINARY]
            if (octeto_bit>-1):
                new_binary=new_binary[0:octeto_bit]
                new_binary=(new_binary)+("0"*(8-len(new_binary)))
            else:
                new_binary="0"*8

        elif (octet>(2**(8-octeto_bit))):
            octeto_bit-=1
            new_binary=ip[1][octeto_mascara] #Last octet doesn't belong completely to mask [BINARY]
            if (octeto_bit>-1):
                new_binary=new_binary[0:octeto_bit+1]
                new_binary+=("0"*(8-len(new_binary)))

        for (i) in range(octeto_mascara+1, len(ip[0])):
            ip[0][i]=0
            ip[1][i]=convert_decimal_to_binary_octet(0)

        if (new_binary is not None):
            ip[1][len(ip)-octeto_mascara]=new_binary
            ip[0][len(ip)-octeto_mascara]=binary_to_decimal(new_binary)
        print ("New major address:", ip)


    subnets=sorted(subnets, key=lambda tup:tup[1], reverse=True)
    return ip, mask, subnets
    
def vlsm(ip, mask, subnets, table=None):
    print ("\nIteracion\n")
    table=table if table else list()
    net=None
    subnet=subnets[0]
    name=subnet[0]
    mask=(32-(subnet[2]))
    print ("Aqui", subnets)
    new_ip=ip.copy()
    del subnets[0]
    print ("0-Redes:",table)
    if (len(table)>0):
        new_ip=add_one_ip(new_ip, mask, table)
        ip=new_ip.copy()
    
    net=[name, new_ip, mask]

    print ("1-Redes:",table)
    table.append(net.copy())
    print ("2-Redes:",table)

    if (len(subnets)>0):
        vlsm(ip.copy(), mask, subnets, table)
    else:
        print (table)
        return table

def add_one_ip(ip, mask, table):
    dec_ip=ip[0]
    bina_ip=ip[1]
    table[-1][1]=[dec_ip, bina_ip]
    print (table)
    new_ip=deepcopy(ip)
    bin_ip=new_ip[1]
    octet=bin_ip[(mask//8)]
    the_rest_before=octet[:((mask%8)-1)]
    the_rest_after=octet[(mask%8):]
    change=octet[(mask%8)-1]
    if (change=='0'):
        change='1'
    print (the_rest_before, change, the_rest_after)
    new_ip[0][mask//8], new_ip[1][(mask//8)]=binary_to_decimal(the_rest_before+change+the_rest_after), the_rest_before+change+the_rest_after
    new_ip=[new_ip[0],new_ip[1]]
    new_ip=new_ip.copy()
    print (table)
    print ("Voy a retornar la ip cambiada:",new_ip)
    return (deepcopy(new_ip))

if (__name__=="__main__"):
    ip, mask, available, subnets=input_data()
    try:
        ip, mask, subnets=beautify(ip, mask, available, subnets)
    except Exception:
        print ("Can't")
    print (vlsm(ip, mask, subnets))