import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])

image= Image.open('https://www.google.com/url?sa=i&url=https%3A%2F%2Faeneas-office.org%2Ffunding%2Fkdt%2F&psig=AOvVaw1nlvJOoTt7eBcN5sF4VfeS&ust=1647896445948000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCKj3jOTK1fYCFQAAAAAdAAAAABAI')
