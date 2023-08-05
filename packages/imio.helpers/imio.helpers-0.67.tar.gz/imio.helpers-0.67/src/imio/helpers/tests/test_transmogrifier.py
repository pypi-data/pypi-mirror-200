# -*- coding: utf-8 -*-
from imio.helpers.testing import IntegrationTestCase
from imio.helpers.transmogrifier import clean_value
from imio.helpers.transmogrifier import correct_path
from imio.helpers.transmogrifier import filter_keys
from imio.helpers.transmogrifier import get_main_path
from imio.helpers.transmogrifier import get_obj_from_path
from imio.helpers.transmogrifier import key_val
from imio.helpers.transmogrifier import pool_tuples
from imio.helpers.transmogrifier import relative_path
from imio.helpers.transmogrifier import str_to_bool
from imio.helpers.transmogrifier import str_to_date

import datetime
import os


# logger simulation for some tests
def logger(item, msg):
    item['errors'] += 1


class TestTesting(IntegrationTestCase):

    def test_clean_value(self):
        self.assertEqual(clean_value(None), None)
        self.assertEqual(clean_value(u'  strip  '), u'strip')
        self.assertEqual(clean_value(u' | strip  ', strip=u' |'), u'strip')
        self.assertEqual(clean_value(u' strip  \n  strip  '), u'strip\nstrip')
        self.assertEqual(clean_value(u' strip  \n  strip  ', osep=u'\r\n'), u'strip\r\nstrip')
        self.assertEqual(clean_value(u' strip  |  strip  ', isep=u'|'), u'strip|strip')
        self.assertEqual(clean_value(u'  \n strip  \n '), u'strip')
        self.assertEqual(clean_value(u' strip  \n "', strip=u' "'), u'strip')
        self.assertEqual(clean_value(u' strip  \n "', patterns=[r'"']), u'strip')
        self.assertEqual(clean_value(u' strip  \n "\'"', patterns=[r'^["\']+$']), u'strip')

    def test_correct_path(self):
        self.assertEquals(correct_path(self.portal, 'abcde'), 'abcde')
        self.assertIn('folder', self.portal.objectIds())
        self.assertEquals(correct_path(self.portal, 'folder'), 'folder-1')
        self.assertEquals(correct_path(self.portal, 'folder/abcde'), 'folder/abcde')
        self.portal.folder.invokeFactory('Document', id='abcde', title='Document')
        self.assertEquals(correct_path(self.portal, 'folder/abcde'), 'folder/abcde-1')
        self.portal.folder.invokeFactory('Document', id='abcde-1', title='Document')
        self.assertEquals(correct_path(self.portal, 'folder/abcde'), 'folder/abcde-2')

    def test_filter_keys(self):
        dic = {'a': 1, 'b': 2, 'c': 3}
        self.assertListEqual(['a', 'b', 'c'], sorted(filter_keys(dic, []).keys()))
        self.assertListEqual([1, 2, 3], sorted(filter_keys(dic, []).values()))
        self.assertListEqual(['a', 'b', 'c'], sorted(filter_keys(dic, ['a', 'b', 'c']).keys()))
        self.assertListEqual([1, 2, 3], sorted(filter_keys(dic, ['a', 'b', 'c']).values()))
        self.assertListEqual(['a', 'c'], sorted(filter_keys(dic, ['a', 'c']).keys()))
        self.assertListEqual([1, 3], sorted(filter_keys(dic, ['a', 'c']).values()))

    def test_get_obj_from_path(self):
        folder = self.portal.folder
        self.assertEqual(get_obj_from_path(self.portal, path='/folder'), folder)
        self.assertEqual(get_obj_from_path(self.portal, path='folder'), folder)
        self.assertEqual(get_obj_from_path(self.portal, path=u'folder'), folder)
        self.assertEqual(get_obj_from_path(self.portal, {'key': 'folder'}, path_key='key'), folder)
        self.assertIsNone(get_obj_from_path(self.portal, {}, path_key='unknown_key'))
        self.assertIsNone(get_obj_from_path(self.portal, path='in_va_lid'))

    def test_get_main_path(self):
        orig_home = os.getenv('INSTANCE_HOME')
        orig_pwd = os.getenv('PWD')
        self.assertEquals(get_main_path('/etc'), '/etc')
        os.environ['INSTANCE_HOME'] = '/etc/parts/xx'
        self.assertEquals(get_main_path(), '/etc')
        os.environ['INSTANCE_HOME'] = '/etc/abcd'
        os.environ['PWD'] = '/myhome'
        self.assertRaisesRegexp(Exception, u"Path '/myhome' doesn't exist", get_main_path)  # path doesn't exist
        self.assertRaisesRegexp(Exception, u"Path '/myhome/toto' doesn't exist", get_main_path, subpath='toto')
        self.assertEquals(get_main_path('/', 'etc'), '/etc')
        os.environ['INSTANCE_HOME'] = orig_home
        os.environ['PWD'] = orig_pwd

    def test_key_val(self):
        dic = {'key': 'val'}
        self.assertEqual(key_val('key', dic), 'val')
        self.assertEqual(key_val('unknown', dic), 'unknown')

    def test_pool_tuples(self):
        lst = [1, 2, 3, 4, 5, 6]
        self.assertEqual(pool_tuples(None, 1), None)
        self.assertListEqual(pool_tuples([], 1), [])
        self.assertListEqual([t for t in pool_tuples(lst, 1)], [(1,), (2,), (3,), (4,), (5,), (6,)])
        self.assertListEqual([t for t in pool_tuples(lst, 2)], [(1, 2), (3, 4), (5, 6)])
        self.assertListEqual([t for t in pool_tuples(lst, 3)], [(1, 2, 3), (4, 5, 6)])
        self.assertListEqual([t for t in pool_tuples(lst, 6)], [(1, 2, 3, 4, 5, 6)])
        with self.assertRaises(Exception) as cm:
            pool_tuples([1, 2, 3], 2, e_msg=u'My pool')
        self.assertEqual(str(cm.exception), "My pool: the given iterable must contain a multiple of 2 elements: "
                         "value = '[1, 2, 3]'")

    def test_relative_path(self):
        self.assertEquals(relative_path(self.portal, '/plone/directory'), 'directory')
        self.assertEquals(relative_path(self.portal, '/alone/directory'), '/alone/directory')

    def test_str_to_bool(self):
        dic = {'True': 'True', 'true': 'true', 'False': 'False', 'false': 'false',
               '0': '0', 0: 0, '1': '1', 123: 123,
               'a': 'a', 'errors': 0}
        self.assertTrue(str_to_bool(dic, 'True', logger))
        self.assertTrue(str_to_bool(dic, 'true', logger))
        self.assertFalse(str_to_bool(dic, 'False', logger))
        self.assertFalse(str_to_bool(dic, 'false', logger))
        self.assertFalse(str_to_bool(dic, '0', logger))  # using fake log method to test error
        self.assertFalse(str_to_bool(dic, 0, logger))
        self.assertTrue(str_to_bool(dic, '1', logger))
        self.assertTrue(str_to_bool(dic, 123, logger))
        self.assertEquals(dic['errors'], 0)
        self.assertFalse(str_to_bool(dic, 'a', logger))
        self.assertEquals(dic['errors'], 1)

    def test_str_to_date(self):
        dic = {1: '2023/03/03', 2: '2023/03/03 09:29', 'errors': 0}
        # str_to_date(item, key, log_method, fmt='%Y/%m/%d', can_be_empty=True, as_date=True, **log_params):
        self.assertIsNone(str_to_date(dic, 'bad_key', logger))
        self.assertRaises(TypeError, str_to_date, dic, 'bad_key', logger, can_be_empty=False)
        ret = str_to_date(dic, 1, logger)
        self.assertIsInstance(ret, datetime.date)
        self.assertEqual(str(ret), '2023-03-03')
        ret = str_to_date(dic, 2, logger, fmt='%Y/%m/%d %H:%M', as_date=False)
        self.assertIsInstance(ret, datetime.datetime)
        self.assertEqual(str(ret), '2023-03-03 09:29:00')
        ret = str_to_date(dic, 2, logger, fmt='%Y/%m/%d %M:%H', as_date=False)
        self.assertEquals(dic['errors'], 1)
