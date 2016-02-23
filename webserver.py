
import bottle
import json
import sys
from bottle import route, run, static_file, template, get, request, error
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from beaker.middleware import SessionMiddleware
import httplib2

import dbquerywrapper

most_recent_keywords = {}
creation_time = 0
user_email = ""
CLIENT_ID = "829051415433-81uvi6gc2ekv4rhrjgp6omrd3ore4g2c.apps.googleusercontent.com"
CLIENT_SECRET = "krBzicGnyG_z1NKr66fMz07v"
PUBLIC_DNS = "http://"+sys.argv[1]+"/"
REDIRECT_URI = PUBLIC_DNS+"redirect"
SCOPE ="https://www.googleapis.com/auth/userinfo.email"
signIn = PUBLIC_DNS+'signIn'
signOut = PUBLIC_DNS+'signOut'



# Configure the SessionMiddleware
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': None,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)


@error(404)
def error404(error):
    return '<h3>Unfortunately, this page does not exist.</h3> <div> <a href="/"><button style="font-weight: bold; color: #ffffff; height: 30px; width: 80px; padding:5px 15px; background:#000000; border:0 none; cursor:pointer; -webkit-border-radius: 5px; border-radius: 5px;" type="button">Return</button></a>'

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@get('/')
def hello():
    #user didn't submit any query or first entry to page.

    global most_recent_keywords
    global user_email

    #result_words empty since no query entered yet
    result_words = []
    #sort the top 20 keywords list
    #most_recent_keywords = sorted(top_keywords,key=lambda l:l[1], reverse=True)
    s = bottle.request.environ.get('beaker.session')
    if 'Logged In' in s and s['Logged_In'] == 'True':
        user_email = ""
    #construct the template using the lists top_keywords and result_words
    return template("main_search_page.html",result_words = result_words,  most_recent = most_recent_keywords, user_email = user_email )

@route('/signIn')
def home():
    global most_recent_keywords
    global user_email
    flow = flow_from_clientsecrets('client_secrets.json',
    scope = 'https://www.googleapis.com/auth/userinfo.email',
    redirect_uri = REDIRECT_URI)
    uri = flow.step1_get_authorize_url()
    #set the session = logged_in
    s = bottle.request.environ.get('beaker.session')
    s['Logged_In'] = 'True'
    s.save()

     # Check to see if a value is in the session
    # user = 'logged_in' in s
    # # Set some other session variable
    # s['user_id'] = 10
    bottle.redirect(str(uri))

@route('/signOut')
def home():
    global user_email
    user_email=""
    s = bottle.request.environ.get('beaker.session')
    s['Logged_In'] = 'False'
    s.save()
    bottle.redirect(str(PUBLIC_DNS))

@route('/redirect')
def redirect_page():
     s = bottle.request.environ.get('beaker.session')
     if  s['Logged_In'] == 'True':
         global user_email
         result_words=[]
         code = request.query.get('code', '')
         global most_recent_keywords
         flow = OAuth2WebServerFlow(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
         scope= SCOPE, redirect_uri=REDIRECT_URI)
         credentials = flow.step2_exchange(code)
         token = credentials.id_token['sub']
         http = httplib2.Http()
         http = credentials.authorize(http)

         #Get user email
         users_service = build('oauth2', 'v2', http=http)
         user_document = users_service.userinfo().get().execute()
         user_email = user_document['email']
         if user_email not in most_recent_keywords:
             most_recent_keywords[user_email] = []

         return template("main_search_page.html", result_words = result_words, most_recent = most_recent_keywords, public_dns=PUBLIC_DNS, user_email = user_email, signIn=signIn, signOut=signOut)
     else:
         bottle.redirect(str(PUBLIC_DNS))

@get('/results')
def do_query():
    #user submitted a query

    global most_recent_keywords
    global user_email
    #get the keywords entered by the user and store into a string
    keywords = request.GET.get('keywords')
    if None == keywords:
        keywords = ""

    keywords = keywords.lower()

    pageid = 0


    try:
        pageid = int(request.GET.get('pageid'))
    except:
        pass
    print "received pageid: " + str(pageid)

    show_next_prev = False
    next_pageid = 0
    prev_pageid = 0

    #separate keywords into words here
    words = keywords.split()

    # this can be used to compute the redirect uri depending on where the server is running
    # so that localhost redirects to localhost and amazon to amazon automatically.
    host = bottle.request.get_header('host')

    # test url list
    url_list = []
    db_query_result = None
    ans = None
    ans2 = None
    allchars = list(keywords)
    a = 0
    b = 0
    op = ""

    # query the db
    if words:
        db_query_result = dbquerywrapper.get_url_list_for_word(words[0])

    for chars in allchars:
        if chars == " ":
            pass
        else:
            try:
                a += int(chars)
                a *= 10
            except ValueError:
                if a!=0:
                    if chars == "+" or chars == "*" or chars == "-" or chars == "/" or chars == "^":
                        op = chars
                        b = a/10
                        a = 0
                    else:
                        break
                elif a!=0 and b!=0:
                    a /= 10
                    if op == "+":
                        ans2 = b+a
                    elif op == "-":
                        ans2 = b-a
                    elif op == "/":
                        ans2 = b/a
                    elif op == "*":
                        ans2 = b*a
                    elif op == "^":
                        ans2 = pow(b, a)
                    if chars == "+" or chars == "*" or chars == "-" or chars == "/" or chars == "^":
                        op = chars
                        b = ans2
                        a = 0
                    else:
                        break
                else:
                    break

    if a!=0 and b!=0:
        a /= 10
        if op == "+":
            ans = b+a
        elif op == "-":
            ans = b-a
        elif op == "/":
            ans = divmod(b, a)
        elif op == "*":
            ans = b*a
        elif op == "^":
            ans = pow(b, a)

    # if len(words) == 3:
    #     if words[1] == "+":
    #         try:
    #             ans = int(words[0]) + int(words[2])
    #         except ValueError:
    #             ans = None
    #
    #     if words[1] == "-":
    #         try:
    #             ans = int(words[0]) - int(words[2])
    #         except ValueError:
    #             ans = None
    #
    #     if words[1] == "/":
    #         try:
    #             ans = int(words[0]) / int(words[2])
    #         except ValueError:
    #             ans = None
    #
    #     if words[1] == "*":
    #         try:
    #             ans = int(words[0]) * int(words[2])
    #         except ValueError:
    #             ans = None
    #
    #     if words[1] == "^":
    #         try:
    #             ans = pow(int(words[0]), int(words[2]))
    #         except ValueError:
    #             ans = None

    # now we have queried the db for result, several possibilities exist
    # if db_query_result is None,
    #    pass empty list to the template and it will show "no result found", leave show_next_prev to False

    # else if len(db_query_result) < 5,
    #  show the results but no next prev buttons

    if not db_query_result:
        show_next_prev = False
        url_list = []
    elif len(db_query_result) <= 5:
        show_next_prev = False
        url_list = db_query_result[:5]
    elif len(db_query_result) > 5 :
        show_next_prev = True
        next_pageid = pageid + 1
        prev_pageid = pageid - 1
        if (prev_pageid < 0):
            prev_pageid = 0
        if (next_pageid*5) >= len(db_query_result):
            next_pageid -= 1

        print "slicing results, nextpageid: " + str(next_pageid) + " prev_pageid: " + str(prev_pageid)

        sliceIdx = pageid*5

        url_list = db_query_result[sliceIdx:sliceIdx+5]

    # make an html from the template.
    return template("search_result.tpl", user_email = user_email, host=host, url_list=url_list,
                    keywords=keywords, show_next_prev=show_next_prev, next_pageid=next_pageid, prev_pageid=prev_pageid, signIn=signIn, signOut=signOut, ans=ans)

@get('/api/json/word_suggestion')
def do_query():
    prefix = request.GET.get('prefix')
    # print prefix
    if None == prefix:
        return "No prefix supplied"

    prefix = prefix.lower()


    result = {}
    #result[prefix] = ["toronto", "test1", "test2"]
    # query the database to find words that match prefix.
    db_words = dbquerywrapper.get_word_list_for_prefix(prefix)

    # print db_words
    result[prefix] = db_words

    return  json.dumps(result)

if '__main__' == __name__ :
    #run(app=app, host='0.0.0.0', port=80, debug=True)
    run(app=app, host='localhost', port=8080, debug=True)
