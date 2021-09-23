import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import graphviz as graphviz

def app(data):
    
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(data, bins=20)
    st.pyplot(fig)
    
    graph = graphviz.Digraph()
    graph.edge('run', 'intr')
    graph.edge('intr', 'runbl')
    graph.edge('runbl', 'run')
    graph.edge('run', 'kernel')
    graph.edge('kernel', 'zombie')
    graph.edge('kernel', 'sleep')
    graph.edge('kernel', 'runmem')
    graph.edge('sleep', 'swap')
    graph.edge('swap', 'runswap')
    graph.edge('runswap', 'new')
    graph.edge('runswap', 'runmem')
    graph.edge('new', 'runmem')
    graph.edge('sleep', 'runmem')
    st.graphviz_chart(graph)

    