# data augmentation

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from ...vis import plot_components_2d
from . import SMOTE

def upsample(target_path, X, y, X_names, method = 'SMOTE', folds = 3, d = 0.5, 
epochs = 10, batch_size = 100, cuda = True, display = False, verbose = True):
    '''
    Upsample a dataset by SMOTE, GAN (todo), Gaussian (todo), or ctGAN.

    Parameters
    ----------
    X_names : the labels for each X feature
    folds : expand to N folds
    d : sampling distance in SMOTE
    epochs, batch_size, cuda : ctgan params
    '''

    if folds == 0:
        return X, y

    if method == 'SMOTE':
        Xn, yn = SMOTE.expand_dataset(X, y, X_names, target_path, d, folds)
    elif method == 'ctGAN':
        from . import ctGAN
        Xn, yn = ctGAN.expand_dataset(X, y, X_names, target_path, folds, epochs, batch_size, cuda, verbose)

    if display:

        pca = PCA(n_components=2) # keep the first 2 components
        X_pca = pca.fit_transform(Xn)
        plot_components_2d(X_pca, yn)
        plt.title('PCA of extended dataset')
        plt.show()

    return Xn, yn