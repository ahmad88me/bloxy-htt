from OpenSSL import SSL

context = SSL.Context(SSL.SSLv23_METHOD)
pkey = 'ssl.key'
cer = 'ssl.cert'
# pkey = 'server.key'
# cer = 'server.crt'
context.use_privatekey_file(pkey)
context.use_certificate_file(cer)
import requests
from flask import Flask, request

app = Flask(__name__)

target_domain = 'https://api.github.com/'


@app.route("/<path:theurl>", methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def red(theurl):
    try:
        print "request headers: " + str(request.headers)
        my_headers = {}
        for hk, hv in request.headers:
            print str(hk) + " => " + str(hv)
            my_headers[hk] = hv
        del my_headers['Host']
        del my_headers['Content-Length']
        del my_headers['Content-Type']
        print 'headers: ' + str(my_headers)
        if request.method == "POST":
            print 'post to: ' + target_domain + theurl
            r = requests.post(target_domain + theurl, data=request.data, headers=my_headers)
            print "post_reply: " + str(r.text)
            return r.text
        elif request.method == "PUT":
            get_url = target_domain + theurl  # + args
            print 'put to: ' + get_url
            print 'put request data: ' + request.data
            print dict(request.form)
            data = request.data
            if request.data == "":
                print 'put request form: ' + str(dict(request.form).keys()[0])
                data = str(dict(request.form).keys()[0])
            r = requests.put(get_url, data=data, headers=my_headers)
            print "put_reply: " + str(r.text)
            return r.text
        elif request.method == "GET":
            args = "?"
            for k in request.args:
                v = request.args[k][0]
                args += str(k) + "=" + str(v) + "&"
            if args[-1] == "&":
                args = args[0:-1]
            if args[-1] == "?":
                args = ""
            get_url = target_domain + theurl + args
            print 'get to: ' + str(get_url)
            r = requests.get(get_url, headers=my_headers)
            print "get_reply: " + str(r.text)
            return r.text
        elif request.method == "DELETE":
            args = "?"
            for k in request.args:
                v = request.args[k][0]
                args += str(k) + "=" + str(v) + "&"
            if args[-1] == "&":
                args = args[0:-1]
            if args[-1] == "?":
                args = ""
            get_url = target_domain + theurl + args
            print 'delete to: ' + str(get_url)
            r = requests.delete(get_url, headers=my_headers)
            print "delete_reply: " + str(r.text)
            return r.text
        else:
            print 'method: ' + str(request.method)
    except Exception as e:
        print "exception: " + str(e)


if __name__ == "__main__":
    app.run(port=80)
# use the below instead of
# app.run(port=5000,ssl_context=context)
# app.run(port=5000,ssl_context=(cer, pkey))
# app.run(port=443,ssl_context=(cer, pkey))
