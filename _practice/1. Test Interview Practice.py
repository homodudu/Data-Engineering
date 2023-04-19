# 1. Reverse String Practice
def rev1(s):
    res = ''
    for i in s:
        res = i + res
    print(res)

def rev2(s):
    print (s[::-1])

def rev3(s):
    dl = ''
    l = [l for l in s]
    l.reverse()
    print(dl.join(l))

rev1('test')
rev2('test')
rev3('test')

# 2. Fizzbang Practice
def f_cond(c):
    if c%5==0 and c%3==0:
        return 'FizzBang'
    elif c%5==0:
        return 'Fizz'
    elif c%5==0:
        return 'Fizz'
    else: return c

def fizzbang(n):
    print([f_cond(f) for f in range(1,n)])

fizzbang(100)

# 3. Fibonacci Practice
def f_gen(n):
    cur,nxt = 0,1
    for _ in range(0,n):
        yield print(cur)
        cur,nxt = nxt,cur+nxt

def fib(n):
    f = f_gen(n)
    for _ in range(0,n):
        f.__next__()

fib(10)

# 4. String 2 List Practice
import re

tests = ['1 vanity fair','3 epicurious','5 ars technica','7 pitchfork','9 architectural digest']

def s_cond(c):
    if re.search(r'\d',c) and int(c)<5:
        return True
    elif re.search(r'\S',c) and re.search(r'\D',c):
        return True
    else: return False

def str2lst(s):
    print([x for x in s if s_cond(x)])

for t in tests:
    str2lst(t)
