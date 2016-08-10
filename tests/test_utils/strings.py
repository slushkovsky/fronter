import unittest
import sys

sys.path.append('../..')
import utils.strings as _us

class TestStrings(unittest.TestCase): 

    def test(self): 
        variants = {
            'CamelCase':        'camel_case', 
            'camelCase':        'camel_case', 
            'CamelCase12345':   'camel_case12345',
            '1camelCase':       '1camel_case',
            'snake_case':       'snake_case', 
            'Camel_snakeCase':  'camel_snake_case', 
            'snakeCamel_Camel': 'snake_camel_camel',
            '__camelCase':      '__camel_case',
            '__CamelCase':      '__camel_case', 
            '_CaMeL':           '_ca_me_l' 
        }

        for camel, snake in variants.items(): 
            try: 
                self.assertEqual(_us.to_snake_case(camel), snake)
            except AssertionError as e: 
                raise AssertionError('[Camel variant: {!r}] '.format(camel) + str(e))


if __name__ == '__main__': 
    unittest.main()