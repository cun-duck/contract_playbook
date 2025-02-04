import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def create_similarity_chart(analysis_data):
    fig = plt.figure(figsize=(6, 3))
    ax = fig.add_subplot(111)
    
    clauses = list(analysis_data.keys())
    similarities = [v['similarity'] for v in analysis_data.values()]
    
    ax.bar(clauses, similarities, color=['#4CAF50','#2196F3','#FF9800'])
    ax.set_ylim(0, 100)
    ax.set_ylabel('Similarity (%)')
    plt.tight_layout()
    
    return fig