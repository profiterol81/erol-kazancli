import math
def poisson_prob(lda):
    # return math.pow(lda, k) * math.pow(math.e, -lda) / math.factorial(k)
    return 1 - math.pow(math.e, -lda)

def bernouilli(lda):
    return float(lda)