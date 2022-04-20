import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])

image= Image.open('
