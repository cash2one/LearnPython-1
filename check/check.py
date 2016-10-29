import urllib2

crawl_timeout = 500


def fetch(userid):
    url = "http://crm.nuomi.com/crm/supplierAccount/syncSupplierAccount.json?userId=" + userid
    try:
        response = urllib2.urlopen(url, timeout=crawl_timeout)
        # print response
        # print userid
        # if response is None:
        #     print('open url %s with urlopen but return null' % url)
        # else:
        #     res_code = response.getcode()
        #     print userid, res_code, response.msg
    except urllib2.HTTPError as error:
        error_info = "The server couldn't fulfill the request, return code: %s", \
                     ", return content: %s" % (error.code, error.read())
        print('open url %s with urlopen error:%s' % (url, error_info))
        # file.write(userid + "\n")
        # file.flush()
    except urllib2.URLError as error:
        error_info = 'Failed to reach the server, and the reason is: %s' % error.reason
        print('open url %s with urlopen error:%s' % (url, error_info))
        # file.write(userid + "\n")
        # file.flush()
    except Exception as error:
        print('open url %s with urlopen error:%s' % (url, error))
        # file.write(userid + "\n")
        # file.flush()


def main():
    file = open("d:\\261")
    # new_file = open("C:\\Users\\sunbeansoft\\Downloads\\missid_3", 'w')
    sum = 0
    for line in file:
        # print line.split("\x01")[0]
        strs = line.split("\n")
        fetch(strs[0])
        sum = sum + 1
        # print sum


if __name__ == "__main__":
    main()
