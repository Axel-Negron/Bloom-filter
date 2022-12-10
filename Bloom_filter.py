import csv
import sys
import array
import math

################################
# Bloom Filter Project #2
#
# Axel Negron Vega  CIIC4025-016
################################


# Functions given
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


def Phase_1(emails_lst):
    """

    Function takes email_list and creates the Bloom filter. Hashing is done by creating k variations of the email
    and setting the bit position of each one by using hash(email_num) % (len(bit_array)*32). 

    Parameters:
    emails_lst: list

    """

    # Constant calculation
    n = len(emails_lst)
    p = 0.0000001
    m = int(math.ceil((n * math.log(p)) / math.log(1 / pow(2, math.log(2)))))
    k = int(round((m / n) * math.log(2)))

    ## Bit array is created of m bit size ##
    bit_array = makeBitArray(m)

    # Iterates through email list and sets it's corresponding bit in bitarray.
    # The position is calculated with hash(email_num) % (len(bit_array)*32).
    # Rather than making k hash functions k entries are made per email using "{}_{}".format(email, _).
    # These are then passed into hash(email_num) % (len(bit_array)*32) to get its bit position.

    for email in emails_lst:
        for _ in range(k):
            email_num = "{}_{}".format(email, _)
            bit_pos = hash(email_num) % (len(bit_array)*32)
            setBit(bit_array, bit_pos)

    return (bit_array, k)


def Phase_2(test_emails, bit_array, k):
    """

    Function takes test_emails and checks if the email is possibly in the bloom filter. Hashing is done by creating k variations of the email
    and setting the bit position of each one by using hash(email_num) % (len(bit_array)*32). 

    Parameters:
    test_emails: list

    """

    # Iterates through check email list and sets it's corresponding bit in bitarray.
    # The position is calculated with hash(email_num) % (len(bit_array)*32).
    # Rather than making k hash functions k entries are made per email using "{}_{}".format(email, _).
    # These are then passed into hash(email_num) % (len(bit_array)*32) to get its bit position.

    for email in test_emails:
        not_in = True
        for _ in range(k):
            email_num = "{}_{}".format(email, _)
            bit_pos = hash(email_num) % (len(bit_array)*32)
            if (testBit(bit_array, bit_pos) == 0):
                print("{},Not in the DB".format(email))
                not_in = False
                break

        if (not_in):
            print("{},Probably in the DB".format(email))


def main():
    """
    Main function gets and parses input files. Creates email list and check list which is then passed to each phase
    """

    if len(sys.argv) > 1:
        in_file = sys.argv[1]
        test_file = sys.argv[2]
        with open(in_file, 'r') as input, open(test_file, "r") as test:
            csvReader = csv.reader(input, delimiter=" ")
            csvCheckReader = csv.reader(test)
            emails = list(csvReader)
            checks = list(csvCheckReader)

            # Creating input lists
            email = [j for i in emails for j in i]
            check = [j for i in checks for j in i]

            # Removing Email from csv files
            email.pop(0)
            check.pop(0)

        # Phase 1 makes and sets bit_array
        (bit_array, k) = Phase_1(email)

        # Phase 2 checks emails in bit_array
        Phase_2(check, bit_array, k)

    else:

        ##Uncomment to test##

        # in_file = os.getcwd()+"\\db_input.csv"
        # test_file = os.getcwd()+"\\db_check.csv"

        # with open(in_file, 'r') as input, open(test_file, "r") as test:
        #     csvReader = csv.reader(input, delimiter=" ")
        #     emails = list(csvReader)
        #     csvCheckReader = csv.reader(test)
        #     checks = list(csvCheckReader)

        #     email = [j for i in emails for j in i]
        #     check = [j for i in checks for j in i]

        # (bit_array, k) = Phase_1(email)
        # Phase_2(check, bit_array, k)
        
        pass


main()
