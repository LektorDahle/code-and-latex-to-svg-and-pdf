import tkinter as tk
import os

class StyleEditor:
    def __init__(self, font_family, font_size, color):
        self.font_family = font_family
        self.font_size = font_size
        self.color = color

    def use(self, input, x, y):
        return (f'<text xml:space="preserve" x="{x}" y="{y}" dominant-baseline="hanging" '
        f'style="font-size:{self.font_size}pt; fill:{self.color}; font-family:\'{self.font_family}\', monospace; white-space:pre;">'
        f'{input}</text>')

class CodeHighlighter:
    def __init__(self):
        self.s = StyleEditor("Clincher Mono", "12", "#ff0000")
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
        parts=[]
        parts.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" xml:space="preserve">'
        )
        parts.append(f'<rect x="0" y="0" width="500" height="500" fill="#ffffff"/>')
        parts.append(self.s.use("Hei", 5, 5))
        parts.append("</svg>")
        svg = "\n".join(parts)
        filename = f'./svg/{self.filename_var.get().strip()}.svg'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename ,"w",encoding="utf-8") as f:
            f.write(svg)



if __name__ == "__main__":
    CodeHighlighter()

