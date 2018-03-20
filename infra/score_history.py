import matplotlib.pyplot as plt


class ScoreHistory:
    def __init__(self):
        self.scores = []

    def append(self, score):
        self.scores.append(score)

    def save_brainplot(self):
        plt.plot(self.scores)
        plt.plot(self.scores)
        plt.ylabel('Average reward score per epochs')
        plt.xlabel('Training epochs')
        plt.title('Training curves tracking the agent average score')
        plt.savefig('saves/Brain_plot.png')
