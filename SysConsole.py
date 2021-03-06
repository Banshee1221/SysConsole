# ToDo: Exception handling
# ToDo: Live display/update

import json
import urllib2

from flask import Flask, render_template, request, redirect, url_for

from sshCommands import *

app = Flask(__name__)
main_url = "/static/img/canvas.png"


# Main pages


@app.route('/')
def main():
    global main_url
    main_url = str(get_wp())
    print main_url
    if main_url == -1:
        main_url = "/static/img/canvas.png"
    return render_template('index.html', wallpaper=main_url)


@app.route('/consolePage')
def console():
    global main_url
    text = json.dumps(getSvnUsers())
    return render_template('consolePage.html', wallpaper=main_url, text=text)


# SVN commands


@app.route('/consolePage/svnAdd', methods=['POST'])
def add_svn_user():

    usr, srv, command = "root", "cpt-svn-02", ""

    fname = request.form.getlist('first_name')[0]
    lname = request.form.getlist('last_name')[0]
    passwd = request.form.getlist('password')[0]
    fname_form = fname.lower().replace(" ", "")
    lname_form = lname.lower().replace(" ", "")

    print "Username: "+fname_form+"."+lname_form+"\nPassword: "+passwd
    print "Executing => echo '"+fname_form+"."+lname_form+" = "+passwd+"' >> /svn/conf/passwd"

    command = "echo '"+fname_form+"."+lname_form+" = "+passwd+"' >> /svn/conf/passwd"

    ssh = ssh_exec(usr, srv, command)

    print "... Done."
    if ssh == 0:
        print "Executing => mkhtpasswd"
    else:
        print "Error executing command, check "+str(srv)+" manually."
        return redirect(url_for('console')) # replace with error page

    command = "sh /svn/conf/mkhtpasswd"

    ssh_exec(usr, srv, command)

    print "... Done."
    print "Account added."

    return redirect(url_for('console'))


@app.route('/consolePage/svnRem', methods=['POST'])
def rem_svn_user():

    usr, srv, command = "root", "cpt-svn-02", ""
    username = request.form.getlist('username')[0].lower().replace(" ", "")

    print "Username: " + username
    print 'Executing => ' + r'sed -i "/\b\(eugene.debeste\)\b/d" /svn/conf/passwd'

    command = r'sed -i "/\b\(eugene.debeste\)\b/d" /svn/conf/passwd'

    ssh_exec(usr, srv, command)

    print "... Done."
    print 'Executing => ' + r'sed -i "/\b\(eugene.debeste\)\b/d" /svn/conf/htpasswd'

    command = r'sed -i "/\b\(eugene.debeste\)\b/d" /svn/conf/htpasswd'

    ssh_exec(usr, srv, command)

    print "... Done."
    print "User was removed."

    return redirect(url_for('console'))


@app.route('/consolePage/svnMod', methods=['POST'])
def mod_svn_user():
    usr, srv, command = "root", "cpt-svn-02", ""
    user = request.form.getlist('username')[0]
    password = request.form.getlist('passwd')[0]
    print "Got password."
    print r"Executing => test=$(grep '" + str(user) + \
          r"' /svn/conf/passwd | grep -Eo '([^ ]|\\ )*$'); sed -i 's/${test}/" + str(password) + r"/g' /svn/conf/passwd"

    command_get = r"grep '" + str(user) + r"' /svn/conf/passwd | grep -Eo '([^ ]|\\ )*$'"
    result = ssh_exec_out(usr, srv, command_get).strip()

    command_change = r"sed -i 's/" + result + "/" + str(password) + r"/g' /svn/conf/passwd"
    ssh_exec(usr, srv, command_change)

    print "... Done."

    return redirect(url_for('console'))


@app.route('/consolePage/git01Add', methods=['POST'])
def git_01_add_key():
    usr, srv = "root", "cpt-git-01"
    print "Getting public key."
    fname = request.form.getlist('first_name')[0]
    lname = request.form.getlist('last_name')[0]
    pubKey = request.form.getlist('pubKey')[0]
    command1 = r"cat /etc/passwd | awk -F: '{print $1}'"
    comm1_out = ssh_exec_out(usr, srv, command1)
    fullname = ("%s.%s" % (fname, lname)).lower().replace(" ", "")

    if fullname not in comm1_out:
        print "Creating user account."
        addComm = "useradd -m -U -k /etc/skel -s /bin/bash %s" % (fullname)
        ssh_exec(usr, srv, addComm)

    print "... Done."
    command2 = r'sed -i %s /home/git/.ssh/authorized_keys; echo command=\"/home/git/bin/gitolite-shell %s\",' \
               r'no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty %s >> ' \
               r'/home/git/.ssh/authorized_keys; echo "# gitolite end" >> /home/git/.ssh/authorized_keys' \
               % ("'$d'", fullname, pubKey)
    print "Executing => " + str(command2)
    ssh_exec(usr, srv, command2)
    print "... Done."

    return redirect(url_for('console'))


@app.route('/consolePage/git03Add', methods=['POST'])
def git_03_add_key():
    usr, srv = "root", "cpt-git-03"
    print "Getting public key."
    fname = request.form.getlist('first_name')[0]
    lname = request.form.getlist('last_name')[0]
    pubKey = request.form.getlist('pubKey')[0]
    command1 = r"cat /etc/passwd | awk -F: '{print $1}'"
    comm1_out = ssh_exec_out(usr, srv, command1)
    fullname = ("%s.%s" % (fname, lname)).lower().replace(" ", "")

    if fullname not in comm1_out:
        print "Creating user account."
        addComm = "useradd -m -U -k /etc/skel -s /bin/bash %s" % (fullname)
        ssh_exec(usr, srv, addComm)

    print "... Done."
    command2 = r'sed -i %s /home/git/.ssh/authorized_keys; echo command=\"/usr/share/gitolite/gl-auth-command ' \
               r'%s\",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty %s >> ' \
               r'/home/git/.ssh/authorized_keys; echo "# gitolite end" >> /home/git/.ssh/authorized_keys' \
               % ("'$d'", fullname, pubKey)
    print "Executing => " + str(command2)
    ssh_exec(usr, srv, command2)
    print "... Done."

    return redirect(url_for('console'))


# General


def get_wp():
    url = 'https://www.reddit.com/r/MinimalWallpaper/random.json'

    try:
        hdr = { 'User-Agent' : 'Prettifier by /u/banshee1221' }
        req = urllib2.Request(url, headers=hdr)
        html = urllib2.urlopen(req).read()
        data = json.loads(html)
        wp = str(data[0]['data']['children'][0]['data']['url'])

        checker = wp.split(".")
        # print checker
        if checker[-1].lower() != "jpg" and checker[-1].lower() != "png":
            newUrl = wp + ".jpg"
            return newUrl
        else:
            return wp
    except urllib2.URLError, e:
        print "Error getting url!"
        return -1


def getSvnUsers():
    usr, srv, command = "root", "cpt-svn-02", ""

    print "Getting List of Users:"
    print 'Executing command => grep -Eo "^[^ ]+" /svn/conf/passwd | grep -v "#"'

    command = r'grep -Eo "^[^ ]+" /svn/conf/passwd | grep -v "#" | sed -n "1!p"'

    out = ssh_exec_out(usr, srv, command)
    out = out.splitlines()

    print "... Done."

    return out


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
