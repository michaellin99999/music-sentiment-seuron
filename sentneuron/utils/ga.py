import numpy as np

class GeneticAlgorithm:
    def __init__(self, neuron, neuron_ix, seq_data, logreg, popSize=100, indSize=1, crossRate=0.95, mutRate=0.1, elitism=3, ofInterest=1.0):
        self.ofInterest   = ofInterest
        self.popSize      = popSize
        self.indSize      = indSize
        self.crossRate    = crossRate
        self.mutRate      = mutRate
        self.elitism      = elitism
        self.neuron       = neuron
        self.seq_data     = seq_data
        self.logreg       = logreg
        self.domain       = (-10, 10)
        self.neuron_ix    = neuron_ix
        self.fits = np.random.uniform(self.domain[0], self.domain[1], (popSize, indSize))
        print(self.fits)

    def calcFitness(self, ind, experiments=30):
        fitness = []
        for i in range(experiments):
            ini_seq = self.seq_data.str2symbols(".")
            gen_seq = self.neuron.generate_sequence(self.seq_data, ini_seq, 256, 1.0, override={self.neuron_ix: ind})

            split = gen_seq.split(" ")
            split = list(filter(('').__ne__, split))
            trans_seq, _ = self.neuron.transform_sequence(self.seq_data, split)

            guess = self.logreg.predict([trans_seq])[0]
            fitness.append((guess - self.ofInterest)**2)

        return sum(fitness)/len(fitness)
        # return (ind - self.ofInterest)**2

    def evaluate(self):
        fitness = []
        for i in range(self.popSize):
            fitness.append(self.calcFitness(self.fits[i][0]))
        return np.array(fitness)

    def cross(self, nextPop):
        for i in range(self.elitism, self.popSize - 1):
            if np.random.random() < self.crossRate:
                nextPop[i] = np.array((nextPop[i] + nextPop[i+1])/2.)

    def mutate(self, nextPop):
        for i in range(self.elitism, self.popSize):
            for gene in range(self.indSize):
                if np.random.random() < self.mutRate:
                    self.fits[i][gene] = np.random.uniform(self.domain[0], self.domain[1])

    def select(self, fitness):
        self.fits = self.fits[fitness.argsort()]
        fitness = fitness[fitness.argsort()]

        nextPop = []
        for i in range(self.popSize):
            if i < self.elitism:
                nextPop.append(self.fits[i])
            else:
                nextPop.append(self.roullete_wheel(fitness))

        return np.array(nextPop)

    def roullete_wheel(self, fitness):
        pick = np.random.uniform(0, sum(fitness))

        current = 0
        for i in range(self.popSize):
            current += fitness[i]
            if current > pick:
                return self.fits[i]

    def evolve(self, epochs=10):
        for i in range(epochs):
            print("-> Epoch", i)
            fitness = self.evaluate()
            nextPop = self.select(fitness)
            print(self.fits)
            print(fitness)
            self.cross(nextPop)
            self.mutate(nextPop)

            self.fits = nextPop

        print("best", self.fits[fitness.argsort()][0])
