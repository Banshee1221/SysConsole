# ToDo: Exception handling
# ToDo: Live display/update

from flask import Flask, render_template, request, redirect, url_for
import json
import urllib2
from sshCommands import *

app = Flask(__name__)
main_url = "../img/canvas.png"


@app.route('/')
def main():
    global main_url
    main_url = str(get_wp())
    print main_url
    if main_url == -1:
        main_url = "../img/canvas.png"
    return render_template('index.html', wallpaper=main_url)


@app.route('/consolePage')
def console():
    global main_url
    return render_template('consolePage.html', wallpaper=main_url)


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


def get_wp():
    url = 'http://www.reddit.com/r/earthporn/random.json'

    try:
        hdr = { 'User-Agent' : 'Prettifier by /u/banshee1221' }
        req = urllib2.Request(url, headers=hdr)
        html = urllib2.urlopen(req).read()
        data = json.loads(html)
        wp = str(data[0]['data']['children'][0]['data']['url'])
        checker = wp.split(".")
        print checker
        if checker[-1].lower() != "jpg" and checker[-1].lower() != "png":
            newUrl = wp + ".jpg"
            return newUrl
        else:
            return wp
    except urllib2.URLError, e:
        print "Error getting url!"
        return -1

if __name__ == '__main__':
    app.run(debug=True)