# -*- coding: utf-8 -*-
# function: lazy import


## ------ System ------
import os
import sys
import gc
import shutil
import time
# from datetime import datetime
from glob import glob
from pathlib import Path


## ------ System Pro ------
import _pickle as pickle
from tqdm import tqdm
from joblib import Parallel, delayed
# from func_timeout import func_set_timeout, func_timeout


## ------ Data Analysis ------
import re
import random
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
# import scienceplots
plt.style.use('ggplot') 
plt.ion()
import seaborn as sns

## ------ Scientific Calculation ------
import math
from decimal import Decimal


## ------ Audio Video ------
# from moviepy.editor import VideoFileClip, AudioFileClip

