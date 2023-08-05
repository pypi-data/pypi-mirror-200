import primes

def primes_cython(n):
    return primes.primes(n)


if __name__ == "__main__":

    print(primes.primes(10))