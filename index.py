#!/usr/bin/python
print 'Content-type: text/html\n'

import hashlib,cgi,cgitb
cgitb.enable()

USERFILE = 'users.txt'

HTML_HEADERS="""
<html>
<head><title>Secure Login</title></head>
<body>
"""
HTML_FOOTERS="""
</body>
</html>
"""

link="""<a href="home.html">Home</a>"""

def getUsers():
    f = open( USERFILE )
    s = f.read()
    f.close()
    userlist = s.split('\n')
    userlist = userlist[:len(userlist)-1]
    userdict = {}
    for user in userlist:
        u = user.split(',')
        userdict[ u[0] ] = u[1]
    return userdict

def login(uname, passw):
    ud = getUsers()
    passw = hashlib.sha1( passw ).hexdigest()
    if uname in ud and passw == ud[uname]:
        return True
    else:
        return False

def register(uname, pw):
    ud = getUsers()
    if uname in ud:
        return False
    else:
        pw = hashlib.sha1( pw ).hexdigest()
        userstring = uname + ',' + pw + '\n'
        f = open('users.txt', 'a')
        f.write( userstring )
        f.close()
        return True


#END FUNCTIONS
#START FLOW OF PROGRAM
    
print HTML_HEADERS + '<center><h1>'

inputs = cgi.FieldStorage()

if 'uname' not in inputs:
    print 'Please enter a username.'

elif 'pw' not in inputs:
    print 'Please enter a password'

else:
    uname = inputs['uname'].value
    pw = inputs['pw'].value

    if 'login' in inputs.keys():
        if login(uname, pw):
            print 'Login Successful'
        else:
            print 'Login Failed'
    
    elif 'register' in inputs.keys():
        if register(uname, pw):
            print 'Registration Successful'
        else:
            print uname + ' is already registered'
        
print '</h1>' + link + '</center>' + HTML_FOOTERS
