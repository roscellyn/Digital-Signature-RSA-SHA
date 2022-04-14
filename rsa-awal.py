from sympy import randprime
from random import randint
from hashlib import sha1
import time

def is_prime(a):
    a_prime = True
    if(a > 1):
        i = 2
        while(a_prime and i <= a//2):
            if(a % i == 0):
                a_prime = False
            i += 1
    else:
        a_prime = False

    return a_prime

def fpb(a, b):
    if(b == 0):
        return a
    else:
        return fpb(b, a % b)
    
def DecToHex(x):
    i = 0
    while ((x // 16**i) != 0):
        i += 1
        
    ArrSize = i
    temp1 = x
    temp2 = x
    Arr = [" " for i in range(ArrSize)]
    
    for i in range(ArrSize-1,-1,-1):
        temp1 = temp1 // 16
        sisa = temp2 % 16
        temp2 = temp1
        if (sisa == 0):
            Arr[i] = "0"
        elif (sisa == 1):
            Arr[i] = "1"
        elif (sisa == 2):
            Arr[i] = "2"
        elif (sisa == 3):
            Arr[i] = "3"
        elif (sisa == 4):
            Arr[i] = "4"
        elif (sisa == 5):
            Arr[i] = "5"
        elif (sisa == 6):
            Arr[i] = "6"
        elif (sisa == 7):
            Arr[i] = "7"
        elif (sisa == 8):
            Arr[i] = "8"
        elif (sisa == 9):
            Arr[i] = "9"
        elif (sisa == 10):
            Arr[i] = 'a'
        elif (sisa == 11):
            Arr[i] = 'b'
        elif (sisa == 12):
            Arr[i] = 'c'
        elif (sisa == 13):
            Arr[i] = 'd'
        elif (sisa == 14):
            Arr[i] = 'e'
        elif (sisa == 15):
            Arr[i] = 'f'

    return "".join(Arr)

def HexToDec(x):
    sum = 0
    for i in range(len(x)):
        if (x[i] == '0'):
            sum = sum + (0 * (16**(len(x)-1-i)))
        elif (x[i] == '1'):
            sum = sum + (1 * (16**(len(x)-1-i)))
        elif (x[i] == '2'):
            sum = sum + (2 * (16**(len(x)-1-i)))
        elif (x[i] == '3'):
            sum = sum + (3 * (16**(len(x)-1-i)))
        elif (x[i] == '4'):
            sum = sum + (4 * (16**(len(x)-1-i)))
        elif (x[i] == '5'):
            sum = sum + (5 * (16**(len(x)-1-i)))
        elif (x[i] == '6'):
            sum = sum + (6 * (16**(len(x)-1-i)))
        elif (x[i] == '7'):
            sum = sum + (7 * (16**(len(x)-1-i)))
        elif (x[i] == '8'):
            sum = sum + (8 * (16**(len(x)-1-i)))
        elif (x[i] == '9'):
            sum = sum + (9 * (16**(len(x)-1-i)))
        elif (x[i] == 'A') or (x[i] == 'a'):
            sum = sum + (10 * (16**(len(x)-1-i)))
        elif (x[i] == 'B') or (x[i] == 'b'):
            sum = sum + (11 * (16**(len(x)-1-i)))
        elif (x[i] == 'C') or (x[i] == 'c'):
            sum = sum + (12 * (16**(len(x)-1-i)))
        elif (x[i] == 'D') or (x[i] == 'd'):
            sum = sum + (13 * (16**(len(x)-1-i)))
        elif (x[i] == 'E') or (x[i] == 'e'):
            sum = sum + (14 * (16**(len(x)-1-i)))
        elif (x[i] == 'F') or (x[i] == 'f'):
            sum = sum + (15 * (16**(len(x)-1-i)))
    
    return (sum)

# Memilih nilai p dan q
p = randprime(2**9, 2**10)
q = randprime(2**9, 2**10)
# p = randint(2**32, 2**33)
# while(not is_prime(p)):
#     p = randint(2**32, 2**33)

# q = randint(2**32, 2**33)
# while(not is_prime(q)):
#     q = randint(2**32, 2**33)

print("p: " + str(p))
print("q: " + str(q))

# Menghitung nilai n dan totient
n = p * q
totient = (p-1) * (q-1)

# Memilih nilai e
e = randint(3, 2**16+1)
while(fpb(totient, e) != 1):
    e = randint(3, 2**16+1)

# Menghitung kunci
k = 1
d = 0.1
while(d%1 != 0):
    d = (1 + k * totient)/e
    k += 1
d = int(d)

# Menyimpan kunci publik dan private
f = open("key.pub", "w")
f.write(str(e) + "," + str(n))
f.close()
f = open("key.pri", "w")
f.write(str(d) + "," + str(n))
f.close()

start_time = time.time()

# Enkripsi file
f = open("text.txt","r")
plain_text = f.read()
f.close()

hash = sha1(plain_text.encode('utf-8'))
digest = hash.hexdigest()

# f.close()
# c_hex = ""
# i = 0
# for byte in file_bytes:
#     c_hex += DecToHex(byte**e % n)
#     if i < len(file_bytes)-1:
#         c_hex += " "
#     # i += 1
# print("cipherteks(hex) = " + c_hex)

# print(HexToDec(digest))
s = HexToDec(digest)**d % n
s_hex = DecToHex(s)
# print(s)

# Menambahkan signature ke file
f = open("text.txt", "a")
text = "\n<ds>" + str(s_hex) + "</ds>" 
f.write(text)
f.close()

# Verifikasi Signature
f = open("text.txt", "r")
file_text = f.read()
sign_message = file_text.split("\n<ds>")
message = sign_message[0]
sign = sign_message[1].split("</ds>")[0]
# print(message)
# print(sign)
f.close()

# hash = sha1(file_bytes)
# digest = hash.hexdigest()
# s = HexToDec(digest)**d % n
# s_hex = DecToHex(s)

print(HexToDec(digest))
print(HexToDec(sha1(message.encode('utf-8')).hexdigest()))
hash_message = HexToDec(sha1(message.encode('utf-8')).hexdigest()) % n
print("Hash message: " + str(hash_message))
hash_sign = HexToDec(sign)**e % n
print("Hash sign: " + str(hash_sign))

if (hash_message == hash_sign):
    print("Tanda tangan digital otentik")
else:
    print("Tanda tangan digital tidak otentik")

# f.close()
# arr_p = []
# for cb in arr_cb:
#     temp = HexToDec(cb)**d % n
#     arr_p.append(temp)
    
# # print("plainteks = ")
# # print(arr_p)
# # print("plainteks(bytes) = ")
# # print(bytearray(arr_p))
# # print(arr_p)
# f = open("plainteks.jpg", "wb")
# arr_pb = bytearray(arr_p)
# # print(len(arr_pb))
# f.write(arr_pb)
# f.close()

# end_time = time.time()
# print("Waktu: " + str(round(end_time - start_time, 2)))