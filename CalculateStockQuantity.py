# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 09:34:54 2018

@author: Rajat Chaudhari

This script is for assessment purposes, problem statement was shared through mail.
"""

import pandas as pd
import json
import os
import gc

#global
filepath = os.getcwd()

def start():
    
    print("The requested files should be in the files folder under main folder, please go thorugh the read me file for folder structure")
    
    i_transactions = input("Enter transaction file name along with extention : ")
    starting_pos = input("Enter start positions file name along with extention : ")
    readfiles(i_transactions, starting_pos)
    del i_transactions, starting_pos
    gc.collect()
    
def readfiles(i_transactions, starting_pos):
    
    '''reading the input files - input transactions and starting positions'''
    
    try:
        with open(filepath + "/files/" + i_transactions, "r") as read_file:
            input_transactions = json.load(read_file)
        input_transactions = pd.DataFrame(input_transactions)
    except Exception as e:
        print("Error in handling transaction file: {}".format(e))
        input_transactions = None
    try:
        start_positions = pd.read_csv(filepath + "/files/" + starting_pos)
    except Exception as e:
        print("Error in handling starting postion file: {}".format(e))
        start_positions = None
    
    if input_transactions is not None and start_positions is not None:
        process(input_transactions, start_positions)   
        del input_transactions, start_positions
    gc.collect()
    
def process(input_transactions, start_positions):
    
    '''If Transaction Type =B ,
           For AccountType=E, Quantity=Quantity + TransactionQuantity
           For AccountType=I, Quantity=Quantity - TransactionQuantity
       If Transaction Type =S ,
           For AccountType=E, Quantity=Quantity - TransactionQuantity
           For AccountType=I, Quantity=Quantity + TransactionQuantity'''
    
    #operations will be performed on new dataframe, the original records will not be affected
    end_positions=start_positions.copy()    
    
    try:        
        for transaction in input_transactions.iterrows():
            if transaction[1]["TransactionType"] == 'B':
                end_positions.loc[(end_positions["Instrument"] == transaction[1][0]) & (end_positions["AccountType"] == "E"), "Quantity"] += transaction[1][2]
                end_positions.loc[(end_positions["Instrument"] == transaction[1][0]) & (end_positions["AccountType"] == "I"), "Quantity"] -= transaction[1][2]
            elif transaction[1]["TransactionType"] == 'S':
                end_positions.loc[(end_positions["Instrument"] == transaction[1][0]) & (end_positions["AccountType"] == "E"), "Quantity"] -= transaction[1][2]
                end_positions.loc[(end_positions["Instrument"] == transaction[1][0]) & (end_positions["AccountType"] == "I"), "Quantity"] += transaction[1][2]
    except Exception as e:
         print("Process Failed: {}".format(e))
         
    end_positions["Delta"] = end_positions["Quantity"] - start_positions["Quantity"]
    try:
        end_positions.to_csv(filepath+"/output/finalposition.txt", sep=',', encoding='utf-8', index=False)
        print("Transactions Processed!")
    except Exception as e:
        print("could not save file, {}".format(e))
    
    print("Instruments with largest net volumes transactions for today \n {}".format(end_positions.loc[end_positions["Delta"]==max(end_positions[end_positions["Delta"]>-1]["Delta"])]))
    print("Instruments with lowest net volumes transactions for today \n {}".format(end_positions.loc[end_positions["Delta"]==min(end_positions[end_positions["Delta"]>-1]["Delta"])]))
    
if __name__=="__main__":
    start()
    
