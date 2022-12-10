import csv
import sys
import os
import array
import math


# Bloom Filter Project #2
#

#
# Axel Negron Vega  CIIC4025-016

# Test func
def makeBitArray(bitSize, fill=0):
    intSize = bitSize >> 5                   # number of 32 bit integers
    if (bitSize & 31):                      # if bitSize != (32 * n) add
        intSize += 1  # a record for stragglers
    if fill == 1:
        fill = 4294967295                                 # all bits set
    else:
        fill = 0                                      # all bits cleared

    bitArray = array.array('I')          # 'I' = unsigned 32-bit integer
    bitArray.extend((fill,) * intSize)
    return (bitArray)

  # testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.


def testBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return (array_name[record] & mask)

# setBit() returns an integer with the bit at 'bit_num' set to 1.


def setBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask
    return (array_name[record])

# clearBit() returns an integer with the bit at 'bit_num' cleared.


def clearBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return (array_name[record])

# toggleBit() returns an integer with the bit at 'bit_num' inverted, 0 -> 1 and 1 -> 0.


def toggleBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] ^= mask
    return (array_name[record])


# Generate input file
# def set_up():
#     set_input(100)

# def random_email_gen(char_num):
#        return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))

# def set_input(len:int):
#     email_lst = []
#     for _ in range(len):

#         email_lst.append(random_email_gen(random.randint(2,15))+"@gmail.com")

#     with open('db_input.csv', 'w', ) as infile:
#         wr = csv.writer(infile)
#         for word in email_lst:
#             wr.writerow([word])


# def Phase_1(in_file):
def Phase_1(emails_lst):
    emails = {}
    for email in emails_lst:
        emails[email] = []

    # with open(in_file,'r') as infile:
    #     database = infile.readlines()[1:]

    # for item in database:
    #     temp = item.replace('\n','')
    #     temp2 = temp.replace('\r','')
    #     if temp == '':
    #         continue
    #     emails[temp2]= []

    # Lectura del input
    # with open(in_file, 'r', ) as infile:

    #     reader = csv.reader(infile, delimiter=' ')
    #     for line in enumerate(reader):
    #         try:
    #             if line[1][0].find('@') == -1:
    #                 continue
    #             line[1][0]
    #             emails[line[1][0]] = []

    #         except:

    #             continue

    n = len(emails)
    p = 0.0000001
    m = int(math.ceil((n * math.log(p)) / math.log(1 / pow(2, math.log(2)))))
    k = int(round((m / n) * math.log(2)))

    bit_array = makeBitArray(m)

    for email in emails:
        num = 0

        for _ in range(k):
            email_num = email+"_"+str(num)
            emails[email].append("{}_{}".format(email, num))
            # emails[email].append(f"{email}_{num}")
            num += 1

    for key in emails:
        values = emails[key]
        for instance in values:
            bit_pos = hash(instance) % (len(bit_array)*32)
            setBit(bit_array, bit_pos)

    # for key in emails:
    #     values = emails[key]
    #     for instance in values:
    #         bit_pos = hash(instance)%len(bit_array)
    #         bit_array[bit_pos] = 1

    return (bit_array, k)


# def Phase_2(test_file,bit_array,k):
def Phase_2(test_emails, bit_array, k):

    test_dict = {}
    for email in test_emails:
        test_dict[email] = []

    # with open(test_file,'r') as infile:
    #     test_Data = infile.readlines()[1:]

    # for item in test_Data:
    #     temp = item.replace('\n','')
    #     temp2 = temp.replace('\r','')
    #     if temp == '':
    #         continue
    #     test_emails[temp2]= []

    # with open(test_file, 'r', ) as infile:

    #     reader = csv.reader(infile, delimiter=' ')
    #     for line in enumerate(reader):
    #         try:
    #             if line[1][0].find('@') == -1:
    #                 continue
    #             line[1][0]
    #             test_emails[line[1][0]] = []

    #         except:
    #             continue

    for email in test_dict:
        num = 0

        for _ in range(k):
            email_num = email+"_"+str(num)
            test_dict[email].append("{}_{}".format(email, num))
            # test_emails[email].append(f"{email}_{num}")
            num += 1

    for key in test_dict:
        mayhaps = True
        values = test_dict[key]
        for instance in values:
            if not mayhaps:
                break
            bit_pos = hash(instance) % (len(bit_array)*32)
            if (testBit(bit_array, bit_pos) == 0):
                mayhaps = False

        if mayhaps:
            print("{},Probably in the DB".format(key))
        else:
            print("{},Not in the DB".format(key))


def main():
    """Main function takes debug conditional. If true a default path is used for csv. Change path to csv name to test
        :param debug:boolean
    """

    if len(sys.argv) > 1:
        in_file = sys.argv[1]
        test_file = sys.argv[2]
        with open(in_file, 'r') as input, open(test_file, "r") as test:
            csvReader = csv.reader(input, delimiter=" ")
            emails = list(csvReader)
            csvCheckReader = csv.reader(test)
            checks = list(csvCheckReader)

            email = [j for i in emails for j in i]
            check = [j for i in checks for j in i]
            email.pop(0)
            check.pop(0)

        (bit_array, k) = Phase_1(email)
        Phase_2(check, bit_array, k)

    else:
        
        in_file = os.getcwd()+"\\db_input.csv"
        test_file = os.getcwd()+"\\db_check.csv"

        with open(in_file, 'r') as input, open(test_file, "r") as test:
            csvReader = csv.reader(input, delimiter=" ")
            emails = list(csvReader)
            csvCheckReader = csv.reader(test)
            checks = list(csvCheckReader)

            email = [j for i in emails for j in i]
            check = [j for i in checks for j in i]

        (bit_array, k) = Phase_1(email)
        Phase_2(check, bit_array, k)
        pass

main()
