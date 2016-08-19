import ConfigParser


def get_config(filename):
    cf = ConfigParser.ConfigParser()
    para_dict = {}
    cf.read(filename)
    para_dict['host'] = cf.get('spider', 'host')
    para_dict['port'] = int(cf.get('spider', 'port'))
    para_dict['user'] = cf.get('spider', 'user')
    para_dict['pwd'] = cf.get('spider', 'pwd')
    para_dict['db'] = cf.get('spider', 'db')
    return para_dict
