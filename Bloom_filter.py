import csv
import sys
import numpy as np
import os
import array
import random
import string
import math
from progress.spinner import MoonSpinner

# Bloom Filter Project #2
#

#
# Axel Negron Vega  CIIC4025-016

#Test func
def makeBitArray(bitSize, fill = 0):
    intSize = bitSize >> 5                   # number of 32 bit integers
    if (bitSize & 31):                      # if bitSize != (32 * n) add
        intSize += 1                        #    a record for stragglers
    if fill == 1:
        fill = 4294967295                                 # all bits set
    else:
        fill = 0                                      # all bits cleared

    bitArray = array.array('I')          # 'I' = unsigned 32-bit integer
    bitArray.extend((fill,) * intSize)
    return(bitArray)

  # testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.
def testBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return(array_name[record] & mask)

# setBit() returns an integer with the bit at 'bit_num' set to 1.
def setBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask
    return(array_name[record])

# clearBit() returns an integer with the bit at 'bit_num' cleared.
def clearBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return(array_name[record])

# toggleBit() returns an integer with the bit at 'bit_num' inverted, 0 -> 1 and 1 -> 0.
def toggleBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] ^= mask
    return(array_name[record])


##Generate input file
def set_up():
    set_input(100)
    
def random_email_gen(char_num):
       return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))

def set_input(len:int)->None:
    email_lst = []
    for _ in range(len):
        
        email_lst.append(random_email_gen(random.randint(2,15))+"@gmail.com")
    
    with open('db_input.csv', 'w', ) as infile:
        wr = csv.writer(infile)
        for word in email_lst:
            wr.writerow([word])
            
        

        


def Phase_1(in_file)->None:
    emails = {}
    with open('db_input.csv', 'r', ) as infile:
 
        reader = csv.reader(infile, delimiter=' ')
        for line in enumerate(reader):
            try: 
              
                line[1][0]
                emails[line[1][0]] = []
            
            except:
                continue

    n = len(emails)
    p = 0.0000001
    m = math.ceil((n * math.log(p)) / math.log(1 / pow(2, math.log(2))))
    k = round((m / n) * math.log(2));
   
    

    bit_array = makeBitArray(m)
    
    for email in emails:
        num = 0

        for _ in range(k):
            emails[email].append(f"{email}_{num}")
            num+=1
           
    
    for key in emails:
        values = emails[key]
        for instance in values:
            bit_pos = hash(instance)%len(bit_array)
            bit_array[bit_pos] = 1
    return (bit_array,k)

    

def Phase_2(test_file,bit_array,k):
    test_emails = {}
    with open(test_file, 'r', ) as infile:
 
        reader = csv.reader(infile, delimiter=' ')
        for line in enumerate(reader):
            try: 
              
                line[1][0]
                test_emails[line[1][0]] = []
            
            except:
                continue

    for email in test_emails:
        num = 0

        for _ in range(k):
            test_emails[email].append(f"{email}_{num}")
            num+=1

    for key in test_emails:
        mayhaps = True
        values = test_emails[key]
        for instance in values:
            if not mayhaps:
                break
            bit_pos = hash(instance)%len(bit_array)
            if (testBit(bit_array,bit_pos)==0):
                mayhaps = False
        
        if mayhaps:
            print(f"{key},Probably in the DB")
        else:
            print(f"{key},Not in the DB")
                
    


def main(debug: bool = True):
    """Main function takes debug conditional. If true a default path is used for csv. Change path to csv name to test
        :param debug:boolean
    """
    try:
    
        ##If in debug comment line below##
        in_file = sys.argv
        pass
        if debug:

            # Change input path to debug
          
            in_file = os.getcwd()+"\\db_input.csv"
            test_file = os.getcwd()+"\\db_check.csv"
            # set_up()
            (bit_array,k) = Phase_1(in_file)
            Phase_2(test_file,bit_array,k)
         

    except:
        ## No file was provided
        pass


main(True)