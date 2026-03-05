import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

class EHOFeatureSelection:
    def __init__(self, n_elephants=10, n_clans=2, n_iter=10):
        self.n_elephants = n_elephants
        self.n_clans = n_clans
        self.n_iter = n_iter
        self.history = []

    def fitness(self, X, y, solution):
        selected = np.where(solution == 1)[0]
        if len(selected) == 0:
            return 0

        X_sel = X[:, selected]

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        scores = cross_val_score(model, X_sel, y, cv=3, scoring="f1_macro")
        return scores.mean()

    def optimize(self, X, y):
        n_features = X.shape[1]
        population = np.random.randint(0, 2, (self.n_elephants, n_features))
        fitness_scores = np.zeros(self.n_elephants)

        for _ in range(self.n_iter):
            for i in range(self.n_elephants):
                fitness_scores[i] = self.fitness(X, y, population[i])

            best_idx = np.argmax(fitness_scores)
            best_solution = population[best_idx]
            best_score = fitness_scores[best_idx]

            self.history.append(best_score)

            for i in range(self.n_elephants):
                if i != best_idx:
                    mask = np.random.rand(n_features) < 0.5
                    population[i] = np.where(mask, best_solution, population[i])

        return best_solution