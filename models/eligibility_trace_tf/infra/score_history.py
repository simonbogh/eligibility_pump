import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

class ScoreHistory:
    def __init__(self):
        self.scores = []

    def append(self, score):
        self.scores.append(score)

    def save_brainplot(self, path, name):
        plt.plot(self.scores, color='red')
        plt.ylabel('Average reward score per epochs')
        plt.xlabel('Training epochs')
        plt.title('Training curves tracking the agent average score')
        plt.savefig(os.path.join(path, str(name) + '.pdf'), format='pdf')