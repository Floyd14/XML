# coding=utf-8
# ITERABLE = oggetto capace di ritornare i membri uno alla volta
# GENERATORE = metodo richiamabule (speciale iteratore)

# Esempio di generatore

'''
Quando metto yield python sa che sto definendo un generatore! (non un metodo normale)

metto yeld => definisco un generatore => implicitamente creo un metodo next()

IMP
next() fa eseguire il codice:

    1- chiama generator()
    2- si esegue il codice fino a yeld
    3- yield ritorna il valore e salva lo stato di generator (tutte le variabili ecc)
    4- chiamo ancora next() che richiama la funzione yeld (IL SECONDO) del generator'''


def generator():
    print("Sto eseguendo il codice")
    num = 3
    print("Esenmpio di variabile al primo next: {}".format(num))
    yield 1

    yield 4
    print("Sono all'ultimo passaggio")

    yield 16


print(generator())  # -> un oggetto speciale

a = generator()  # lo istanzio

# Chiamo il metodo next
print(next(a))  # -> 1
print(next(a))  # -> 4
print(next(a))  # -> 16
# print(next(a))  # -> raise StopIteration

# Può essere usato nei cicli for
# chiama tutte le volte la funzione next() del generatore.. e assegna il valore di yeld a i
print("\nIn for loop:")
for i in generator():
    print(i)

# Solitamente può essere usato con la funzione list()
# ....
print("\nWith list() method")
list(generator())


# ESEMPIO 2 - ref: https://wiki.python.org/moin/Generators

# Simple script
print("\nESEMPIO2:")


def return_first_n(n):
    # ritorna una lista di n elementi
    num, nums = 0, []
    while num < n:
        nums.append(num)
        num += 1
    return nums

sum_of_first_n = sum(return_first_n(1000000))
print("Normal method:{}".format(sum_of_first_n))


# Using the generator pattern (an iterable)
#
class ReturnFirstN(object):

    def __init__(self, n):
        self.n = n
        self.num, self.nums = 0, []

    def __iter__(self):
        return self

    # Compatybily with python 3x (python 3x doesn't have __next__() builtin method)
    def __next__(self):
        return self.next()

    def next(self):
        if self.num < self.n:
            current, self.num = self.num, self.num+1
            return current
        else:
            raise StopIteration()


sum_of_first_n2 = sum(ReturnFirstN(1000000))
print("With class (generator) method:{}".format(sum_of_first_n2))
