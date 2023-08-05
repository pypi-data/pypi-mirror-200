from .primes import primes

def primes_cython(n):
    return primes(n)


if __name__ == "__main__":

    print(primes(10))