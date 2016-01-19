from flask import Flask, render_template, request, redirect, url_for
import json
import urllib2
from sh import ssh

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
    fname = request.form.getlist('first_name')[0]
    lname = request.form.getlist('last_name')[0]
    passwd = request.form.getlist('password')[0]
    fname_form = fname.lower().replace(" ", "")
    lname_form = lname.lower().replace(" ", "")

    print "Username: "+fname_form+"."+lname_form+"\nPassword: "+passwd
    print "Executing => echo '"+fname_form+"."+lname_form+" = "+passwd+"' >> /svn/conf/passwd"
    ssh_conn = ssh("root@cpt-svn-02", "echo '"+fname_form+"."+lname_form+" = "+passwd+"' >> /svn/conf/passwd")
    print "... Done\nExecuting => mkhtpasswd"
    ssh_conn = ssh("root@cpt-svn-02", "sh /svn/conf/mkhtpasswd")
    print ssh_conn

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