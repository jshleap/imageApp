"""
App to add multiple images and visualize them
"""
import mpld3
import streamlit as st
from imageio import volread
from matplotlib import pyplot as plt, colors
from streamlit.components.v1 import html

st.markdown(""" <style> .font {
font-size:35px ; font-family: 'Gene-Condensed-Bold'; color: #005596;} 
</style> """, unsafe_allow_html=True)
files = None
fig = plt.figure(figsize=(9, 9))
plt.axis('off')
with st.sidebar:
    st.markdown('<p class="font">Image Overlay</p>', unsafe_allow_html=True)
    st.write("Use this simple app to explore images collected from pooled screens")
    files = st.file_uploader('', accept_multiple_files=True, type=['jpg', 'png', 'jpeg', 'tif'])
    if files:
        #cols = st.columns(len(files))
        images = []
        for idx, f in enumerate(files):
            ck = st.checkbox(f.name, value=idx==0)
            sl = st.slider('Transparency', 0., 1., 0.1, key=idx)
            cmap = st.selectbox("Colormap", options=['viridis', 'inferno', 'Greys', 'Reds', 'Blues', 'Greens',
                                                            'black', 'red', 'blue', 'green'], index=0,
                                       key=f'cmap_{idx}')
            norm = None
            if cmap in ['black', 'red', 'blue', 'green']:
                cmap = colors.ListedColormap(['white', cmap])
                norm = colors.BoundaryNorm([0, 10], cmap.N)
            if ck:
                img = volread(f)
                if len(img.shape) == 4:
                    sl2 = st.slider('Cycles/Rounds', 0, img.shape[0]-1, 1, key=f'cycle_idx')
                    img = img[sl2]
                if len(img.shape) == 3:
                    sl3 = st.slider('Channel', 0, img.shape[0] - 1, 1, key=f'channel_idx')
                    img = img[sl3]

                images.append(img)
                plt.imshow(img, alpha=sl, cmap=cmap, norm=norm)
if files:
    fig_html = mpld3.fig_to_html(fig)
    html(fig_html, height=2048, width=2048)
