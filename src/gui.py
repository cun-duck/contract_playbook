import PySimpleGUI as sg
import pdfplumber
from .api_client import ClauseAPIClient
from .clause_analyzer import ClauseAnalyzer
from .visualization import create_similarity_chart, draw_figure

sg.theme('LightGreen')

layout = [
    [sg.Text("Contract File"), sg.Input(key="-FILE-"), sg.FileBrowse()],
    [sg.Button("Analyze", size=(10,1)), sg.Button("Exit", size=(10,1))],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Multiline(size=(80,10), key="-REPORT-", font=('Courier', 10))],
    [sg.StatusBar("", key="-STATUS-")]
]

window = sg.Window("Contract Clause Analyzer", layout, finalize=True)
canvas_elem = window["-CANVAS-"]
fig_canvas_agg = None

api_client = ClauseAPIClient()
analyzer = ClauseAnalyzer()

while True:
    event, values = window.read(timeout=100)
    
    if event == "Analyze":
        window["-STATUS-"].update("Processing...")
        
        try:
            if values["-FILE-"].endswith('.pdf'):
                with pdfplumber.open(values["-FILE-"]) as pdf:
                    text = "\n".join([p.extract_text() for p in pdf.pages[:10]])
            else:
                with open(values["-FILE-"]) as f:
                    text = f.read()
            
            extracted = api_client.extract_clauses(text)
            
            analysis = {}
            for clause_type, content in extracted.items():
                ideal = analyzer.get_ideal_clause(clause_type)
                comparison = analyzer.compare_clauses(content, ideal)
                analysis[clause_type] = comparison
            
            report = "\n".join([
                f"{ct.upper()}\nSimilarity: {res['similarity']}%\nDifferences: {', '.join(res['differences'][:3])}\n"
                for ct, res in analysis.items()
            ])
            
            if fig_canvas_agg:
                fig_canvas_agg.get_tk_widget().destroy()
            
            fig = create_similarity_chart(analysis)
            fig_canvas_agg = draw_figure(canvas_elem.TKCanvas, fig)
            
            window["-REPORT-"].update(report)
            window["-STATUS-"].update("Analysis Complete")
            
        except Exception as e:
            window["-STATUS-"].update(f"Error: {str(e)}")
    
    if event in (sg.WIN_CLOSED, "Exit"):
        break

window.close()