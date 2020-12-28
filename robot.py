from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient(host="10.162.0.148", port=502)


def get_input():
    return client.read_coils(0,16).bits



def set_output(num):
    b = get_input()
    if num < 0:
        client.write_coils(0, [False] * 16)
        return
    b[num] = not b[num]
    client.write_coils(0, b)

