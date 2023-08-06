"""
r_em network suites designed to restore different modalities of electron microscopy data

Author: Ivan Lobato
Email: Ivanlh20@gmail.com
"""
import os
import pathlib
from typing import Tuple

import h5py
import numpy as np

def fcn_set_gpu_id(gpu_visible_devices: str = "0") -> None:
    """
    Set GPU id for Tensorflow.

    :param gpu_visible_devices: A string representing the GPU id.
    """
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_visible_devices

def load_network(model_name: str = 'hrstem', gpu_id: str = "0"):
    """
    Load r_em neural network model.

    :param model_name: A string representing the name of the model.
    :param gpu_id: A string representing the GPU id.
    :return: A tensorflow.keras.Model object.
    """
    model_name = model_name.lower()
    
    fcn_set_gpu_id(gpu_id)
    
    model_path = pathlib.Path(__file__).resolve().parent / 'models' / model_name

    import tensorflow as tf
    model = tf.keras.models.load_model(model_path, compile=False)
    model.compile()
    return model

def load_test_data(model_name: str = 'hrstem') -> Tuple[np.ndarray, np.ndarray]:
    """
    Load test data for r_em neural network.

    :param model_name: A string representing the name of the model.
    :return: A tuple containing two numpy arrays representing the input (x) and output (y) data.
    """
    model_name = model_name.lower()
    
    path = pathlib.Path(__file__).resolve().parent / 'test_data' / f'{model_name}.h5'

    with h5py.File(path, 'r') as h5file:
        x = np.asarray(h5file['x'][:], dtype=np.float32).transpose(0, 3, 2, 1)
        y = np.asarray(h5file['y'][:], dtype=np.float32).transpose(0, 3, 2, 1)
    
    return x, y
