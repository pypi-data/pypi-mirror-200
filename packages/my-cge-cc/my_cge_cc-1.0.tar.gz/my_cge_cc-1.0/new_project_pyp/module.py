ef fib(n):
    if n <= 1:
        return n
    else:
        return fib(n -1) + (n -2)