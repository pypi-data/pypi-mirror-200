"""Tools for reshaping the higher dimensions of NIfTI-MRS

    Author: Will Clarke <william.clarke@ndcn.ox.ac.uk>
    Copyright (C) 2021 University of Oxford
"""
from nifti_mrs.nifti_mrs import NIFTI_MRS

import numpy as np

# TO DO:
# def _reshape_hdr(dynamic_hdr, target):

#     return reshaped_hdr


def reshape(nmrs, reshape, d5=None, d6=None, d7=None):
    """Reshape the higher dimensions (5-7) of an nifti-mrs file.
    Uses numpy reshape syntax to reshape. Use -1 for automatic sizing.

    If the dimension exists after reshaping a tag is required. If None is passed
    but one already exists no change will be made. If no value exists then an
    exception will be raised.

    :param nmrs: Input NIfTI-MRS file
    :type nmrs: NIFTI_MRS
    :param reshape: Tuple of target sizes in style of numpy.reshape, higher dimensions only.
    :type reshape: tuple
    :param d5: Dimension tag to set dim_5, defaults to None
    :type d5: str, optional
    :param d6: Dimension tag to set dim_6, defaults to None
    :type d6: str, optional
    :param d7: Dimension tag to set dim_7, defaults to None
    :type d7: str, optional
    """

    shape = nmrs[:].shape[0:4]
    shape += reshape
    nmrs_reshaped = NIFTI_MRS(np.reshape(nmrs[:], shape), header=nmrs.header)

    # reshpaed_hrd = _reshape_hdr(nmrs_reshaped.dynamic_hdr_vals[2],)

    # Note numerical index is N-1
    if d5:
        nmrs_reshaped.set_dim_tag(4, d5)
    elif nmrs_reshaped.ndim > 4\
            and nmrs.dim_tags[0] is None:
        raise TypeError(f'An appropriate d5 dim tag must be given as ndim = {nmrs_reshaped.ndim}.')
    if d6:
        nmrs_reshaped.set_dim_tag(5, d6)
    elif nmrs_reshaped.ndim > 5\
            and nmrs.dim_tags[1] is None:
        raise TypeError(f'An appropriate d6 dim tag must be given as ndim = {nmrs_reshaped.ndim}.')
    if d7:
        nmrs_reshaped.set_dim_tag(6, d7)
    elif nmrs_reshaped.ndim > 6\
            and nmrs.dim_tags[2] is None:
        raise TypeError(f'An appropriate d7 dim tag must be given as ndim = {nmrs_reshaped.ndim}.')

    return nmrs_reshaped
