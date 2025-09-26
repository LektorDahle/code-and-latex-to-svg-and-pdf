import tkinter as tk

class CodeHighlighter:
    def __init__(self):
        self.build_ui()
    
    def build_ui(self):
        self.root = tk.Tk()
        bar = tk.Frame(self.root)
        bar.pack(fill = "x", padx = 8, pady = 8)
        tk.Label(bar, text = "Filename: ").pack(side = "left")
        self.filename_var = tk.StringVar(value = "New File")
        tk.Entry(bar, textvariable = self.filename_var, width = 28).pack(side = "left", padx = (6, 12))
        tk.Button(bar, text = "Compiler", command = self.compile).pack(side = "left")

        self.txt = tk.Text(self.root, width = 100, height = 40, undo = True)
        self.txt.pack(fill = "both", expand = True, padx = 8, pady = (0, 8))

        self.root.mainloop()
    def compile(self):
        pass

if __name__ == "__main__":
    CodeHighlighter()

