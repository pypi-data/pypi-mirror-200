#!/usr/bin/env python
# coding: utf-8

# # How to store/retrieve a `Detector` object
# 
# In this how-to guide we will see how to store an existing `Detector` object (e.g. a `CCD` detector) into a file (e.g. hdf5) and how to load a file into a new `Detector` object.
# 
# By the end of the lesson you will know how to:
# * Save a `CCD` detector object into a HDF5 file with method `Detector.to_hdf5`
# * Load a `CCD` detector object from a HDF5 file with method `Detector.from_hdf5`
# 
# To create the `CCD` detector object, we will run the simple pipeline from the [first simulation pipeline](https://gitlab.com/esa/pyxel-data/-/blob/master/tutorial/01_first_simulation.ipynb).

# ## Get a new CCD detector object
# 
# We are going to create a new CCD detector object based on our [first simulation pipeline](https://gitlab.com/esa/pyxel-data/-/blob/master/tutorial/01_first_simulation.ipynb).
# 
# ### Run a simple pipeline
# 
# Run a simple pipeline to create a new `CCDDetector` object.

# In[1]:


import pyxel

# Load the configuration file
config = pyxel.load("exposure.yaml")

# Run the pipeline
result = pyxel.exposure_mode(
    exposure=config.exposure,
    detector=config.ccd_detector,
    pipeline=config.pipeline,
)

result


# In[ ]:


# Get the detector object
detector = config.ccd_detector

detector


# ### Display detector

# In[ ]:


pyxel.display_detector(detector)


# ## Store 'detector' into a HDF5 file

# In[ ]:


def get_file_size(filename):
    """Display filename's size."""
    import os

    size = os.path.getsize(filename) / 1024 / 1024
    print(f"Size of file {filename!r}: {size:.2f} MB")


# In[ ]:


detector.to_hdf5("ccd.h5")


# In[ ]:


get_file_size("ccd.h5")


# ## Create a new detector from the HDF5 file

# In[ ]:


from pyxel.detectors import Detector

new_detector = Detector.from_hdf5("ccd.h5")

new_detector


# ### Check if the detector is valid

# In[ ]:


detector == new_detector


# ### Display the new detector

# In[ ]:


pyxel.display_detector(new_detector)


# ## Open the HDF5 file

# In[ ]:


import h5py

f = h5py.File("ccd.h5")

f


# In[ ]:


# Get attributes
dict(f.attrs)


# In[ ]:


# Get list of datasets
list(f)


# In[ ]:


list(f["/data"])


# In[ ]:


# Get a dataset
f["/data/image"]


# In[ ]:


import numpy as np

np.array(f["/data/image"])


# In[ ]:


f.close()


# In[ ]:




