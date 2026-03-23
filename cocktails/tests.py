import psutil
import socket

addrs = psutil.net_if_addrs()

for ad in addrs.get('Беспроводная сеть'):
    if ad.family == socket.AF_INET:
        print(ad.address)

# for interface, addr_list in addrs.items():
#
#     for addr in addr_list:
#         if addr.family == socket.AF_INET:
#             print(f"{interface}: {addr.address}")