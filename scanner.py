import asyncio
import socket
import shutil
from progress.bar import IncrementalBar

checked = 0
cols = shutil.get_terminal_size().columns
bar = IncrementalBar(max=65536)


def checkIp(ip):
    try:
        sum = 0
        if ip == 'localhost':
            return True
        parts = ip.split(".", 4)
        if len(parts) == 4:
            for part in parts:
                part = int(part)
                if -1 < part < 256:
                    sum += 1
        else:
            return False
        if sum != 4:
            return False
    except ValueError:
        return False


async def check(host, port, free):
    global checked, cols, bar
    sock = socket.socket()
    try:
        await sock.connect((host, port))
    except TypeError:
        print(f" <-- Port {port} Opened")
        free.append(port)
    except OSError:
        pass
    finally:
        bar.next()
        checked += 1
        sock.close()


async def main(host):
    free = []
    t = []
    for port_number in range(65536):
        t.append(check(host, port_number, free))
    await asyncio.wait(t)
    bar.finish()
    free = sorted(free)
    fin = ','.join(str(i) for i in free)
    print(f'Free => { fin }')

host = input('Host Name/IP-Address: ')
if checkIp(host):
    asyncio.run(main(host))
else:
    print("Wrong Input")
