import tkinter as tk
from tkinter import font as tkfont
import os
import json, pathlib
_STYLES_PATH = pathlib.Path(__file__).with_name("styles.json")


class StyleEditor:
    def __init__(self, font_family, font_size, color, weight = 400):
        self.font_family = font_family
        self.font_size = font_size
        self.color = color
        self.weight = weight
        root = tk.Tk()
        f = tkfont.Font(family = self.font_family, size = self.font_size)
        self.character_width = f.measure("0"*100) / 100
        self.line_height = f.metrics("linespace")
        root.destroy()

    def use(self, input, x, y):
        return (f'<text xml:space="preserve" x="{x}" y="{y}" dominant-baseline="hanging" '
        f'style="font-size:{self.font_size}pt; fill:{self.color}; font-family:\'{self.font_family}\', monospace; font-weight: {self.weight}; white-space:pre;">'
        f'{input}</text>')

class NewStyle:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.geometry("1200x50")
        tk.Label(self.root, text = "Style Name: ").pack(side = "left")
        self.stylename = tk.StringVar(master = self.root, value = "New Style")
        tk.Entry(self.root, textvariable = self.stylename, width = 28).pack(side = "left", padx = (6, 12))
        
        tk.Label(self.root, text = "Family: ").pack(side = "left")
        self.font_family = tk.StringVar(master = self.root, value = "Arial")
        tk.Entry(self.root, textvariable = self.font_family, width = 28).pack(side = "left", padx = (6, 12))
        
        tk.Label(self.root, text = "Size: ").pack(side = "left")
        self.font_size = tk.StringVar(master = self.root, value = "12")
        tk.Entry(self.root, textvariable = self.font_size, width = 10).pack(side = "left", padx = (6, 12))
        
        tk.Label(self.root, text = "Color: ").pack(side = "left")
        self.color = tk.StringVar(master = self.root, value = "#000000")
        tk.Entry(self.root, textvariable = self.color, width = 10).pack(side = "left", padx = (6, 12))
        
        tk.Label(self.root, text = "Weight: ").pack(side = "left")
        self.weight = tk.StringVar(master = self.root, value = "400")
        tk.Entry(self.root, textvariable = self.weight, width = 10).pack(side = "left", padx = (6, 12))
        
        tk.Button(self.root, text = "Add style", command = self.add_style).pack(side = "left")
        self.root.mainloop()

    def add_style(self):
        name = self.stylename.get().strip()
        spec = {
            "font_family": self.font_family.get().strip(),
            "font_size_pt": int(self.font_size.get()),
            "color": self.color.get().strip(),
            "weight": int(self.weight.get()),
            }
        try:
            with open(_STYLES_PATH, "r", encoding = "utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"schema_version": 1, "styles": {}}

        data["styles"][name] = spec

        with open(_STYLES_PATH, "w", encoding = "utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.root.destroy()

class GREP:
    

class CodeHighlighter:
    def __init__(self):
        self.line_height = 1.65*12
        self.get_styles()
        self.build_ui()
    
    def load_styles(self, path: str | pathlib.Path = _STYLES_PATH):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("styles", {})

    def get_styles(self):
        styles = self.load_styles()
        for name, spec in styles.items():
            setattr(self, name, StyleEditor(
             font_family = spec["font_family"],
             font_size = spec["font_size_pt"],
             color = spec["color"],
             weight = spec["weight"],
            ))

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
        tk.Button(bar, text = "New Style", command=lambda: NewStyle(self.root)).pack(side = "left")

        self.root.mainloop()

    def compile(self):
        raw = self.txt.get("1.0", "end-1c")
        lines = raw.splitlines() or [""]
        expanded = [l.replace("\t", "    ") for l in lines]
        parts = []
        parts.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" xml:space="preserve">')
        parts.append(f'<rect x="0" y="0" width="500" height="500" fill="#ffffff"/>')
        row = 5
        for i in expanded:
            col = 5
            for j in i.split(" "):
                char_width = 0
                if j == "jeg" or j == "Jeg":
                    parts.append(self.comment.use(j, col, row))
                    char_width = self.comment.character_width
                else:
                    parts.append(self.default.use(j, col, row))
                    char_width = self.default.character_width
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

