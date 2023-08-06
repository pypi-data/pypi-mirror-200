"""
Set of Metric Utility Functions
"""
import numpy as np
import os
import zipfile
import tempfile

def calculate_sparsity(arr: np.ndarray) -> float:
    """
    Calculates the Sparsity Level (0-1) of a numpy weight matrix.
    
    Args:
        `arr` (np.ndarray): The Array.
    
    Returns:
        (float): The Sparsity Value of `arr` (`sparsity` == 1 --> 100% sparse matrix). 
    """
    # Calculate the sparsity percentage
    sparsity = 1.0 - np.count_nonzero(arr) / arr.size
    return sparsity

def get_gzipped_model_size(file: str) -> float:
  """
  Calcualites the Size of the Comprressed version of the file.

  Args:
      `file` (str): File to Calculate Size.
  
  Returns:
      (float): Size of compressed file in terms of number of bytes.
  """
  _, zipped_file = tempfile.mkstemp('.zip')
  with zipfile.ZipFile(zipped_file, 'w', compression=zipfile.ZIP_DEFLATED) as f:
    f.write(file)
  return os.path.getsize(zipped_file)