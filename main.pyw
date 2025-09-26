import tkinter as tk
from tkinter import font as tkfont
import os

class StyleEditor:
    def __init__(self, font_family, font_size, color, weight = 400):
        self.font_family = font_family
        self.font_size = font_size
        self.color = color
        self.weight = weight
        root = tk.Tk()
        f = tkfont.Font(family=self.font_family, size=self.font_size)
        self.character_width = f.measure("0"*100) / 100
        self.line_height = f.metrics("linespace")
        root.destroy()

    def use(self, input, x, y):
        return (f'<text xml:space="preserve" x="{x}" y="{y}" dominant-baseline="hanging" '
        f'style="font-size:{self.font_size}pt; fill:{self.color}; font-family:\'{self.font_family}\', monospace; font-weight: {self.weight}; white-space:pre;">'
        f'{input}</text>')

class CodeHighlighter:
    def __init__(self):
        self.line_height = 1.65*12
        self.s = StyleEditor("Clincher Mono", "12", "#ff0000")
        self.r = StyleEditor("Clincher Mono", "12", "#33ff00")
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
        raw = self.txt.get("1.0", "end-1c")
        lines = raw.splitlines() or [""]
        expanded = [l.replace("\t", "    ") for l in lines]
        

        parts=[]
        parts.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" xml:space="preserve">'
        )
        parts.append(f'<rect x="0" y="0" width="500" height="500" fill="#ffffff"/>')
        row = 5
        for i in expanded:
            col = 5
            for j in i.split(" "):
                char_width = 0
                if j == "jeg" or j == "Jeg":
                    parts.append(self.r.use(j, col, row))
                    char_width = self.r.character_width
                else:
                    parts.append(self.s.use(j, col, row))
                    char_width = self.s.character_width
                col += len(j) * char_width + char_width
            row += self.line_height
        parts.append("</svg>")
        svg = "\n".join(parts)
        filename = f'./svg/{self.filename_var.get().strip()}.svg'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename ,"w",encoding="utf-8") as f:
            f.write(svg)



if __name__ == "__main__":
    CodeHighlighter()

