#!/usr/bin/env python3

### Validate URLs found in markdown documents using HEAD requests

import sys, markdown, requests, bs4 as BeautifulSoup

headers = {'User-Agent':
           'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'}

requests.packages.urllib3.disable_warnings() # we're disabling HTTPS 

def check_url(url):
    return requests.head(url, allow_redirects=True, headers=headers, verify=False) \
        or requests.get(url, allow_redirects=True, headers=headers, verify=False)

def retrieve_urls(filename):
    with open(filename) as fd:
        mdtext = fd.read()
        html_text = markdown.markdown(mdtext)
        soup = BeautifulSoup.BeautifulSoup(html_text, "html.parser")
        return [a['href'] for a in soup.findAll('a')]

def check_urls(filename):
    print ('checking URLs for %s' % (filename,))
    ok = True
    for url in retrieve_urls(filename):
        msg = 'Checking %s =>' % (url,)
        try:
            response = check_url(url)
        except Exception as e:
            print ('%s FAILED (%s)' % (msg, e))
            ok = False
        else:
            if response:
                print ('%s OK' % (msg,))
            else:
                print ('%s FAILED (%s: %s)' % (msg, response.status_code, response.reason))
                ok = False
    return ok

def main():
    ok = True
    for filename in sys.argv[1:]:
        try:
            ok &= check_urls(filename)
        except IOError as e:
            print (e)
            ok = False
    exit (0 if ok else 1)

if __name__ == '__main__':
    main()
