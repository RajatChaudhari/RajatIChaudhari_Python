# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 10:03:32 2018

@author: Rajat Chaudhari

Test Script to test the final output of the Stock Process
"""

import unittest
import pandas as pd
import os

class TestStockQuantityProcess(unittest.TestCase):
    
    filepath = os.getcwd()

    def setup(self):
        '''takes the expected file and caculated end of day position file'''
        
        expected_pos = input("Enter expected position file name along with extention : ")
        calculated_pos = input("Enter start positions file name along with extention : ")
        
        try:
            expected_positions = pd.read_csv(self.filepath + "/files/" + expected_pos)
        except Exception as e:
            print("Error in handling starting postion file: {}".format(e))
            expected_positions = None
        try:
            calculated_positions = pd.read_csv(self.filepath + "/output/" + calculated_pos)
        except Exception as e:
            print("Error in handling starting postion file: {}".format(e))
            calculated_positions = None
        
        if expected_positions is not None and calculated_positions is not None:
            self.test_recordsmatch(expected_positions, calculated_positions)
            self.test_recordsdontmatch(expected_positions, calculated_positions)
                
    def test_recordsmatch(self, expected_positions,calculated_positions):        
        self.assertDictEqual(expected_positions.to_dict(), calculated_positions.to_dict(), "Check the Process Logic")
    
    def test_recordsdontmatch(self, expected_positions,calculated_positions):        
        self.assertEqual(expected_positions.iloc[1][3], calculated_positions.iloc[0][3], "This was expected as we are comapring values from different rows")

if __name__ == "__main__":
    
    a=TestStockQuantityProcess()
    a.setup()