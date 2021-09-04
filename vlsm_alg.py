from prettytable import PrettyTable
from math import log2, ceil


def validate_oct(oct):
    return (oct <= 255) and (oct >= 0)


def suma_binaria(bin1, bin2):
    return bin(int(bin1, 2) + int(bin2, 2))[2:].zfill(8)


def to_binaryOctet(num):
    return bin(num)[2:].zfill(8)


def to_Decimal(bin):
    return int(bin, 2)


def input_data():
    ip = input("Major net address: ")
    # Check it's correct
    ip = list(map(int, ip.split(".")))
    while not (sum(list(map(validate_oct, ip))) == 4 and len(ip) == 4):
        ip = input("Not a valid ip address, try again: ")
        ip = list(map(int, ip.split(".")))

    # convert correct ip to binary representation and append that
    ip = [ip, list(map(to_binaryOctet, ip))]

    mask = int(input("Net-Mask (Bits): "))
    while (mask > 32) or (mask < 0):
        mask = int(input("Not correct, try again. Net-Mask (Bits): "))

    # Number of available hosts
    available = (2 ** (32 - mask)) - 2

    subnet_number = int(input("Number of subnets: "))
    subnets = list()
    tot = 0
    for i in range(subnet_number):
        name = input("Enter name of subnet " + str(i + 1) + ": ") or (
            "Subnet " + str(i + 1)
        )
        num_desired = int(input("Number of hosts of subnet '" + name + "': "))
        bits = ceil(log2(num_desired + 2))
        num_required = 2 ** bits - 2
        tot += num_required
        subnets.append((name, num_desired, num_required, bits))
    subnets.append(tot)

    return ip, mask, available, subnets


def validate_possible(ip, mask, available, subnets):
    if available < subnets[-1]:
        return False
    if mask % 8 == 0:
        for i in range(mask // 8, 4):
            if ip[0][i] > 0:
                return False
    else:
        if (
            (ip[0][mask // 8] < (2 ** (8 - mask % 8)) and ip[0][mask // 8] > 0)
            or (ip[0][mask // 8] > (256 - 2 ** (8 - mask % 8)))
            or (
                ip[0][mask // 8] < (2 ** (8 - mask % 8))
                and ip[0][mask // 8] > (256 - 2 ** (8 - mask % 8))
            )
        ):
            return False
        for i in range(mask // 8 + 1, 4):
            if ip[0][i] > 0:
                return False
    return True


def subnet_mask(bits_host):
    return 32 - bits_host


def next_net(ip, new_mask):
    print(ip, ip[-1], ip[-1][new_mask // 8])
    adding = "1" + "0" * (8 - new_mask % 8)
    new = ip[-1][new_mask // 8]
    new = suma_binaria(new, adding)
    if (to_Decimal(new)>255):
        new=new[-8:]
        ip[-1][(new_mask//8)-1]=suma_binaria(ip[-1][(new_mask//8)-1],"1")
        ip[0][(new_mask//8)-1]=to_Decimal(ip[-1][(new_mask//8)-1])
    ip[-1][new_mask // 8] = new
    ip[0][new_mask // 8] = to_Decimal(new)
    return ip


def VLSM():
    try:
        ip, mask, available, subnets = input_data()
        while not validate_possible(ip, mask, available, subnets):
            print("The desired VLSM is not possible, please try again...\n\n\n")
            ip, mask, available, subnets = input_data()
        del subnets[-1]  # Delete total used directions
        subnets.sort(key=lambda y: y[-3], reverse=True)
        print("Ordered subnets:", subnets)
        print("Net mask:", mask)
        net_ips = list()
        for i, subnet in enumerate(subnets):
            new_net_mask = subnet_mask(subnet[-1])
            if i == 0:
                new_ip = ip
            else:
                if new_net_mask == net_ips[-1][-2]:
                    ip = next_net(ip, new_net_mask)
                new_ip = ip
            print(
                subnet,
                "\n",
                subnet[0],
                ":\n",
                "\tBits for host:",
                subnet[-1],
                "\n\tIP:",
                ip,
                "\n\tSubnet mask:",
                new_net_mask,
                "\n",
            )
            net_ips.append(
                (
                    str(i + 1) + ". " + subnet[0],
                    subnet[1],
                    ".".join(list(map(str, new_ip[0]))),
                    new_net_mask,
                    subnet[2],
                )
            )
            try:
                if subnet_mask(subnets[i + 1][-1]) != new_net_mask:
                    ip = next_net(ip, new_net_mask)
            except:
                pass

        make_files(net_ips)
        return net_ips

    except:
        print("An error ocurred, please try again...")


def make_files(net_ips):
    table = PrettyTable(
        [
            "Name",
            "Desired number of hosts",
            "IP",
            "Netmask",
            "Total number of hosts available on subnet",
        ]
    )
    table.add_rows(net_ips)
    with open("index.html", "w") as f:
        f.write("<html>")
        f.write("<head>")
        f.write("<title>")
        f.write("VLSM results")
        f.write("</title>")
        f.write("</head>")
        f.write("<body>")
        f.writelines(table.get_html_string(format=True))
        f.write("</body>")
        f.write("</html>")
    with open("table.json", "w") as f:
        f.writelines(table.get_json_string(format=True, indent=4))
    with open("table.csv", "w") as f:
        f.writelines(table.get_csv_string(format=True))
    with open("table.txt", "w") as f:
        f.writelines(table.get_string(format=True))


if __name__ == "__main__":
    # Driver code -- testing
    print(VLSM())
