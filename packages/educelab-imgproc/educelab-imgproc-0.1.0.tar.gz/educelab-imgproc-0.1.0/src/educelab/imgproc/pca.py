import numpy as np
from sklearn.decomposition import IncrementalPCA, PCA


def fit(x, components: int = None, batch_size: int = None,
        incremental: bool = False, roi=None):
    # Validate number of components
    if components is not None and not (1 < components < x.shape[0]):
        raise ValueError(f'Requested components ({components}) outside '
                         f'range [1, {x.shape[0]}]')

    # Setup new PCA
    if incremental:
        pca = IncrementalPCA(n_components=components,
                             batch_size=batch_size)
    else:
        pca = PCA(n_components=components)

    # Crop training data to ROI
    if roi is not None:
        x = x[:, roi.y:roi.y + roi.h, roi.x:roi.x + roi.w]

    # Flatten input
    x_flat = x.reshape((x.shape[0], -1))
    x_flat = np.swapaxes(x_flat, 0, 1)

    # Fit input files
    pca.fit(x_flat)
    return pca


def apply_transform(x, pca):
    # Transform images
    x_flat = x.reshape((x.shape[0], -1))
    x_flat = np.swapaxes(x_flat, 0, 1)
    x_flat = pca.transform(x_flat)

    # Convert back to images
    x_flat = np.swapaxes(x_flat, 0, 1)
    pca_shape = (pca.n_components_,) + x.shape[1:]
    return x_flat.reshape(pca_shape)
