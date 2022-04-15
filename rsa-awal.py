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

# Memilih nilai p dan q secara random
p = randprime(2**9, 2**10)
q = randprime(2**9, 2**10)

print("p: " + str(p))
print("q: " + str(q))

# Menghitung nilai n dan totient
n = p * q
totient = (p-1) * (q-1)

# Menghitung kunci publik
e = randint(3, 2**16+1)
while(fpb(totient, e) != 1):
    e = randint(3, 2**16+1)

# Menghitung kunci private
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
# Membaca pesan awal dari file
f = open("text.txt","r")
message = f.read()
f.close()

# Membaca kunci private dari file
f = open("key.pri","r")
file_pkey = f.read()
private_key = int(file_pkey.split(",")[0])
private_n = int(file_pkey.split(",")[1])
f.close()

# Menghitung hash dari pesan awal
hash = sha1(message.encode('utf-8'))
digest = hash.hexdigest()

# Menghitung sign dari hash
s = HexToDec(digest)**private_key % private_n
s_hex = DecToHex(s)

# Menambahkan sign ke file
f = open("text.txt", "a")
text = "\n<ds>" + str(s_hex) + "</ds>" 
f.write(text)
f.close()

# Verifikasi Signature
# Membaca pesan dan sign dari file
f = open("text.txt", "r")
file_text = f.read()
sign_message = file_text.split("\n<ds>")
verif_message = sign_message[0]
verif_sign = sign_message[1].split("</ds>")[0]
# print(message)
# print(sign)
f.close()

# Membaca public key dari file
f = open("key.pub","r")
file_key = f.read()
public_key = int(file_key.split(",")[0])
public_n = int(file_key.split(",")[1])
f.close()

# Menghitung hash dari pesan dan signature
hash_message = HexToDec(sha1(verif_message.encode('utf-8')).hexdigest()) % n
hash_sign = HexToDec(verif_sign)**public_key % n
# print("Hash message: " + str(hash_message))
# print("Hash sign: " + str(hash_sign))

if (hash_message == hash_sign):
    print("Tanda tangan digital otentik")
else:
    print("Tanda tangan digital tidak otentik")