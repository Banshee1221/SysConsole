from sh import ssh


def ssh_exec(user, server, command):
    ssh_conn = ssh(user+"@"+server, command)
    print "SSH Command complete. Code: " + str(ssh_conn.exit_code)
    return ssh_conn.exit_code
