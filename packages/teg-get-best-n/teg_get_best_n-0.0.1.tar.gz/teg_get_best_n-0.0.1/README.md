Module of functions for estimating the optimal number of components or clusters.

# PCA

Selects the number of components based on comparing eigenvectors between split-halves of the data. I.e., this doesn't use the shape of the eigenvalue curve, but makes a split between components with high versus low split-half similarity.

Usage:

O = teg_get_best_n.get_n_components(X)

This returns a dictionary with the estimated number of components in O['nComponents'], as well as the eigenvalues (O['eigenvalues']) and eigenvectors (O['eigenvectors']).

The file example.py contains tests with simulated data to check how well the true number of latent variables is recovered.
