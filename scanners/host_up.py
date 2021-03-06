# Rohin Dasari and Ben Hiner
import socket
from color import pcolor
from scanners import tcp_connect, udp_connect, ping_os, icmp_echo, icmp_timestamp, tcp_privileged

def run(targets, is_admin):
    targets_up = set()
    if is_admin:
        # Try an ICMP echo request (PING), TCP SYN to port 443, 
        # TCP ACK to port 80, and an ICMP timestamp request
        icmp_echo_targets_up = icmp_echo.run(targets, print_results=False)
        targets_up.update(icmp_echo_targets_up)
        tcp_syn_targets_up, tcp_syn_ports_open = tcp_privileged.syn.run(targets, [443], options = [1, 2, 3, 4, 5], fragment_size=None, print_results=False)
        targets_up.update(tcp_syn_targets_up)
        tcp_ack_targets_up = tcp_privileged.ack.run(targets, [80], options = [2, 3, 4, 5], fragment_size=None, print_results=False)
        targets_up.update(tcp_ack_targets_up)
        icmp_timestamp_targets_up = icmp_timestamp.run(targets, print_results=False)
        targets_up.update(icmp_timestamp_targets_up)
    else:
        # Unprivileged
        # Use TCP connect() scan on two common ports so as to not look suspicious
        check_tcp_ports = [80, 443]
        tcp_connect_targets_up, tcp_connect_ports_open = tcp_connect.run(targets, check_tcp_ports, print_results=False)
        targets_up.update(tcp_connect_targets_up)
        ping_os_targets_up = ping_os.run(targets, print_results=False, verbose=False)
        targets_up.update(ping_os_targets_up)

    print_results(targets_up)
    return targets_up

def print_results(targets_up):
    # Print results
    print('Done detecting hosts.')
    print('Hosts that are up:') 
    print(f'{pcolor.color.OPEN}{targets_up}{pcolor.color.CLEAR}')
