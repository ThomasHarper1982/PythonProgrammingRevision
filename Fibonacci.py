def Fibonacci(n, K):
    if K.__contains__(n):
        return K[n]

    result = 0
    if n==1 or n==2:
        result = 1
    else:
        result =  Fibonacci(n-1,K) + Fibonacci(n-2,K)
    K[n] = result
    return result


if __name__ == '__main__':

    K = dict()
    n = 137

    result = Fibonacci(n, K)
    print(result)


