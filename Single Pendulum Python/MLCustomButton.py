import tkinter as tk

class CustomButton(tk.Canvas):
    
    def __init__(self, parent, text, command,
                 bg="royalblue", fg="white", font=None, width=100, height=24, radius=20):
        super().__init__(
            parent,
            bg=parent.cget("bg"),
            width=width,
            height=height,
            highlightthickness=0,
            relief="flat",
            cursor="hand2")
        self._text = text
        self._font = font or ("Segoe UI", 10)
        self._radius = radius
        self._width = width
        self._height = height
        self.bind("<ButtonPress-1>",   self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self._command = command
        self._bg = bg
        self._fg = fg
        self._draw(bg)
    def _round_rect(self, x1, y1, x2, y2, r, **kwargs):
        """Dessine un rectangle aux coins arrondis sur le canvas."""
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,   x2, y1+r,
            x2, y2-r,
            x2, y2,   x2-r, y2,
            x1+r, y2,
            x1, y2,   x1, y2-r,
            x1, y1+r,
            x1, y1,   x1+r, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    def _draw(self, fill):
        self.delete("all")
        self._round_rect(1, 1, self._width-1, self._height-1,
                         self._radius, fill=fill, outline=self._darken(fill), width=2)
        self.create_text(self._width//2, self._height//2,
                         text=self._text, fill=self._fg,
                         font=self._font, anchor="center")
    def _darken(self, color):
        r, g, b = self.winfo_rgb(color)
        r, g, b = r // 256, g // 256, b // 256
        return f"#{int(r*0.8):02x}{int(g*0.8):02x}{int(b*0.8):02x}"
    def _on_press(self, event):
        self._draw(self._darken(self._bg))

    def _on_release(self, event):
        self._draw(self._bg)
        self._command()

