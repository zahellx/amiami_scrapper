import unittest
import pandas as pd
import project.utils.utilidades as utilities
import numpy as np

class Utilidades(unittest.TestCase):
    
    def test_compare_df(self):
        #Caso 1
        a1 = {
            'name': ['Arroz', 'pollo', 'ostias', 'agua', 'zapatos'],
            'image': ['Arroz', 'pollo', 'ostias', 'agua', 'zapatos'],
            'price': ['Arroz', 'pollo', 'ostias', 'agua', 'zapatos'],
            'brand': ['Arroz', 'pollo', 'ostias', 'agua', 'zapatos'],
            }
        dfA1 = pd.DataFrame(data=a1)
        b1 = {
            'name': ['Arroz', 'pollo', 'ostias'],
            'image': ['Arroz', 'pollo', 'ostias'],
            'price': ['Arroz', 'pollo', 'ostias'],
            'brand': ['Arroz', 'pollo', 'ostias'],
            }
        dfB1 = pd.DataFrame(data=b1)
        diff_df1 = utilities.compare_df(dfA1, dfB1)
        print(diff_df1)
        res = [['agua','agua', 'agua', 'agua'], ['zapatos','zapatos', 'zapatos', 'zapatos']]
        self.assertEqual(diff_df1, res)
        #Caso 2
        a2 = {
            'name': ['Arroz', 'pollo', 'ostias', 'agua'],
            'image': ['Arroz', 'pollo', 'ostias', 'agua'],
            'price': ['Arroz', 'pollo', 'ostias', 'agua'],
            'brand': ['Arroz', 'pollo', 'ostias', 'agua'],
            }
        dfA2 = pd.DataFrame(data=a2)
        b2 = {
            'name': ['Arroz', 'pollo', 'ostias'],
            'image': ['Arroz', 'pollo', 'ostias'],
            'price': ['Arroz', 'pollo', 'ostias'],
            'brand': ['Arroz', 'pollo', 'ostias'],
            }
        dfB2 = pd.DataFrame(data=b2)
        diff_df2 = utilities.compare_df(dfA2, dfB2)
        print(diff_df2)
        self.assertEqual(diff_df2, [['agua','agua', 'agua', 'agua']])
        #Caso 3
        a3 = {
            'name': ['Arroz', 'pollo', 'ostias'],
            'image': ['Arroz', 'pollo', 'ostias'],
            'price': ['Arroz', 'pollo', 'ostias'],
            'brand': ['Arroz', 'pollo', 'ostias'],
            }
        dfA3 = pd.DataFrame(data=a3)
        b3 = {
            'name': ['Arroz', 'pollo', 'ostias'],
            'image': ['Arroz', 'pollo', 'ostias'],
            'price': ['Arroz', 'pollo', 'ostias'],
            'brand': ['Arroz', 'pollo', 'ostias'],
            }
        dfB3 = pd.DataFrame(data=b3)
        diff_df3 = utilities.compare_df(dfA3, dfB3)
        print(diff_df3)
        self.assertEqual(diff_df3, [])



if __name__ == '__main__':
    unittest.main()