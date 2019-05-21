import random
import numpy as np
import math
import prob as pr
from matplotlib import pyplot as plt

def calculate_infections(population, infections, infected, lda):
    new_infected = []
    # for i in population:
    #     if infections[i] == 1:
    #         rd = random.random()
    #         for j in population:
    #             if infections[j] == 0:
    #                 prb = pr.bernouilli(lda*math.pow((math.fabs(j-i)), -3))
    #                 if rd < prb:
    #                     new_infected.append(i)
    # for i in population:
    #     if infections[i] == 0:
    #         for j in population: # check all the infected agents to see if any one of them infect the non-infected agent
    #             if infections[j] == 1:
    #                 rd = random.random()
    #                 # prb = pr.poisson_prob(lda*math.pow((math.fabs(j-i)), -3), 1) # poisson prob to be infected by this agent
    #                 prb = pr.bernouilli(lda*math.pow((math.fabs(j-i)), -3)) # poisson prob to be infected by this agent
    #                 if rd < prb:
    #                     new_infected.append(i)
    #                     break; # if infected do not look further, mark as infected
    # infected = np.where(np.array(infections) == 1)[0]
    # for i in population:
    #     if infections[i] == 0:
    #         lda_acc = 0
    #         rd = random.random()
    #         start = 0
    #         end = len(population)
    #         if i - 10 > 0:
    #             start = i - 10
    #         if i + 10 < len(population):
    #             end = i + 10
    #         for j in range(start, end):
    #             if infections[j] == 1:
    #         # for j in infected:
    #                 lda_acc += lda*math.pow((math.fabs(j-i)), -3)
    #         # prb = pr.bernouilli(lda_acc)
    #         prb = pr.poisson_prob(lda_acc)
    #         if rd < prb:
    #             new_infected.append(i)
    lambdas = np.zeros(1000)
    infected = np.where(np.array(infections) == 1)[0]
    for i in infected:
        start = 0
        end = len(population)
        if i - 5 > 0:
            start = i - 10
        if i + 5 < len(population):
            end = i + 5
        for j in range(start, end):
            if infections[j] == 0:
                lambdas[j] += lda*math.pow((math.fabs(j-i)), -3)
    for k in population:
        if lambdas[k] > 0:
            rd = random.random()
            prob = pr.poisson_prob(lambdas[k])
            if rd < prob:
                new_infected.append(k)

    return new_infected

def calculate_healings(population, infections, lda, gen):
    healings = []
    if gen < 100:
        first = 1
    else:
        first = 0
    for i in population[first:]:
        if infections[i] == 1:
            rd = random.random()
            prb = pr.poisson_prob(lda)
            # prb = pr.bernouilli(lda)
            if rd < prb:
                healings.append(i)
    return healings


def main():
    n_pop = 1000
    population = range(0, n_pop)
    increment = 5 * math.pow(10, -3)
    lda1 = math.pow(10, -4) - increment # lambda for infection
    gens = []
    n_steps = 120
    n_time = 10000
    for step in range(0, n_steps):
        print(step)
        infections = list(np.zeros(n_pop).astype(int))
        infections[0] = 1
        lda1 += increment # increment lambda
        lda2 = 1
        print ("Lambda:" + str(lda1))
        gen_found = n_time
        infected = [0]
        for gen in range(n_time):
            # print(gen)
            new_infections = calculate_infections(population, infections, infected, lda1)
            # infected = infected + new_infections
            healings = calculate_healings(population, infections, lda2, gen)
            # for h in healings:
            #     infected.remove(h)
            for i in new_infections:
                infections[i] = 1
            for i in healings:
                infections[i] = 0
            sum_infections = sum(infections)
            if sum_infections == n_pop:
                print ("All infected after generation " + str(gen))
                gen_found = gen
                break;
            elif sum_infections == 0:
                print ("All healed after generation " + str(gen))
                gen_found = gen
                break;
        print ("Some infected:" + str(sum_infections))
        gens.append(gen_found)
    plt.plot(np.arange(0,n_steps), gens)
    plt.title("Number of generations to heal vs. lambda")
    plt.xlabel("lambda = 0.0001 + x * 0.005")
    plt.ylabel("Number of generations to heal")
    plt.ylim([0,10000])
    plt.xlim([0, n_steps])
    plt.show()
    plt.savefig("plot.png")
    return infections

infections = main()
# print(infections)




