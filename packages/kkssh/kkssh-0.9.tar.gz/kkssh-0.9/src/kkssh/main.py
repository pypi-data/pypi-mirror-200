import os
import argparse
import paramiko


def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        dp[i][0] = i
    
    for j in range(1, n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    return dp[m][n]

def connect(host: str):
    os.system('ssh %s' % host)

def format_hostname(cfg: dict):
    if cfg is None:
        cfg = {}
    hostname = cfg.get('hostname', ' ')
    port = cfg.get('port', '22')
    username = cfg.get('user', ' ')
    if port != '22':
        return f'{username}@{hostname}:{port}'
    return f'{username}@{hostname}'

def connect_to_user_selected(hosts: list[str], ssh_config: paramiko.SSHConfig):
    # Let user select
    print('#\tHost\tHostName')
    for idx in range(len(hosts)):
        host = hosts[idx]
        cfg = ssh_config.lookup(host)
        formated_hostname = format_hostname(cfg)
        print(f'{idx}\t{host}\t{formated_hostname}')
    print('Select Index: [0]', end =" ")
    selected_idx = input()
    if not selected_idx:
        selected_idx = 0
    try:
        selected_idx = int(selected_idx)
    except Exception:
        print('Index must be an integer')
        return
    if selected_idx >= len(hosts):
        print(f'Index must be less than {len(hosts)}')
        return
    # Connect
    host = hosts[selected_idx]
    connect(host)

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
                        prog='kkssh',
                        description='ssh wrapper')

    parser.add_argument('-c', '--config', required=False, default='~/.ssh/config')
    parser.add_argument('hostname', nargs='?')
    args = parser.parse_args()
    ssh_config_path = args.config
    target_host = args.hostname

    # Load ssh config
    ssh_config = paramiko.SSHConfig()
    with open(ssh_config_path) as f:
        ssh_config.parse(f)
    hosts = sorted([i for i in ssh_config.get_hostnames() if i != '*' ])

    # No hostname provided, let user select
    if not target_host:
        connect_to_user_selected(hosts, ssh_config)
        return

    # Direct connect if hostname match
    if target_host in hosts:
        cfg = ssh_config.lookup(target_host)
        print(f'connecting to {format_hostname(cfg)}')
        connect(target_host)
        return

    # Find alternatives
    hosts_with_distance = []
    for host in hosts:
        distance = edit_distance(target_host, host)
        if distance < max(len(host), len(target_host)):
            hosts_with_distance.append([host, distance])
    hosts_with_distance = sorted(hosts_with_distance, key=lambda x: x[1])
    if not hosts_with_distance:
        print('Not found')
        return
    hosts = [i[0] for i in hosts_with_distance]
    connect_to_user_selected(hosts, ssh_config)
    

if __name__ == '__main__':
    main()
