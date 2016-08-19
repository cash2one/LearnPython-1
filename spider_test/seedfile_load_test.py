# -*- coding: utf-8 -*-
'''
    @author: aijie
'''
import spider.seedfile_load
import spider.config_load
import unittest  
  
class TestSeedFileLoadFunctions(unittest.TestCase):  
    '''
    seedfile_load文件测试类
    '''
    def setUp(self):  
        self.data = ["http://pycm.baidu.com:8081"]
        config = spider.config_load.ConfigObject()
        config.setconfig('spider.conf')
  
    def test_get_seedfile(self):
        '''
        获取种子文件测试方法
        '''  
        lines = spider.seedfile_load.get_seedfile()
        if lines is None:
            self.assertEqual(lines, None)
        else:
            for line in lines:
                index = self.data.index(line)
                self.assertEqual(line, self.data[index])
  
if __name__ == '__main__':  
    unittest.main() 
