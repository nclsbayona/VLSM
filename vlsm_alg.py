from prettytable import PrettyTable
from math import log2, ceil
from copy import deepcopy

def validate_oct(oct):
    return (oct<=255) and (oct>=0)

def suma_binaria(bin1, bin2):
	return bin(int(bin1, 2)+int(bin2, 2))[2:].zfill(8)

def to_binaryOctet(num):
	return bin(num)[2:].zfill(8)
    
def to_Decimal(bin):
	return int(bin, 2)

def input_data():
    ip=input("Major net address: ")
    #Check it's correct
    ip=list(map(int, ip.split('.')))
    while (not (sum(list(map(validate_oct, ip)))==4 and len(ip)==4)):
        ip=input("Not a valid ip address, try again: ")
        ip=list(map(int, ip.split('.')))

    #convert correct ip to binary representation and append that
    ip=[ip, list(map(to_binaryOctet, ip))]

    mask=int(input("Net-Mask (Bits): "))
    while ((mask>32) or (mask<0)):
        mask=int(input("Not correct, try again. Net-Mask (Bits): "))

    #Number of available hosts
    available=(2**(32-mask))-2

    subnet_number=int(input("Number of subnets: "))
    subnets=list()
    tot=0
    for i in range(subnet_number):
        name=input("Enter name of subnet "+str(i+1)+": ") or ("Subnet "+str(i+1))
        num_desired=int(input("Number of hosts of subnet '"+name+"': "))
        bits=ceil(log2(num_desired+2))
        num_required=2**bits-2
        tot+=num_required
        subnets.append((name, num_desired, num_required, bits))
    subnets.append(tot)

    return ip, mask, available, subnets

def validate_possible(ip, mask, available, subnets):
    if (available<subnets[-1]):
        return False
    if (mask%8==0):
        for i in range (mask//8, 4):
            if (ip[0][i]>0):
                return False
    else:
        if ((ip[0][mask//8]<(2**(8-mask%8)) and ip[0][mask//8]>0) or (ip[0][mask//8]>(256-2**(8-mask%8))) or (ip[0][mask//8]<(2**(8-mask%8)) and ip[0][mask//8]>(256-2**(8-mask%8)))):
            return False
        for i in range (mask//8+1, 4):
            if (ip[0][i]>0):
                return False
    return True

def subnet_mask(bits_host):
    return 32-bits_host

def VLSM():
    try:
        ip, mask, available, subnets=input_data()
        while (not validate_possible(ip, mask, available, subnets)):
            print ("The desired VLSM is not possible, please try again...\n\n\n")
            ip, mask, available, subnets=input_data()
        del subnets[-1] # Delete total of used directions
        subnets.sort(key=lambda y: y[-2], reverse=True)
        print (subnets)
        #Missing
        print ("Mascara de red:", mask)
        for subnet in (subnets):
            print (subnet,'\n', subnet[0],':\n', "\tBits para host:", subnet[-1], "\n\tMascara de subred:", subnet_mask(subnet[-1]), '\n')

    except:
        print ("An error ocurred, please try again...")


if __name__=="__main__":
    #Driver code -- testing
    VLSM()