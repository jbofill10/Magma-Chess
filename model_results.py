import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.style as style

style.use('seaborn-poster')

def run():

    with open('Data/model_results', 'rb') as file:
        history = pickle.load(file)
        print(history)

        sns.lineplot(x=list(range(10)), y=history['loss'])
        plt.xticks(list(range(10)), list(range(1, 11)))
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Model Loss')
        plt.savefig('Data/model_loss.png')
        plt.close()

        sns.lineplot(x=list(range(10)), y=history['acc'])
        plt.xticks(list(range(10)), list(range(1, 11)))
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.title('Model Accuracy')
        plt.savefig('Data/model_acc.png')


if __name__ == '__main__':
    run()