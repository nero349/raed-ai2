
import ast
import operator
import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

APP_NAME = "RAED AI"
DB_FILE = "raed_memory.db"

# Operaciones matemáticas permitidas
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod,
}


def calculate(expression):
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            if abs(left) > 1e100 or abs(right) > 1e100:
                raise ValueError("Número demasiado grande")
            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponente demasiado grande")
            return OPS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](evaluate(node.operand))
        raise ValueError("Operación no permitida")

    result = evaluate(tree)
    if isinstance(result, float) and not result.is_integer():
        return round(result, 8)
    return int(result) if isinstance(result, float) else result


class RaedAI:
    def __init__(self, root):
        self.root = root
        root.title("RAED AI | Asistente personal")
        root.geometry("850x600")
        root.minsize(600, 450)
        root.configure(bg="#080d18")

        self.db = sqlite3.connect(DB_FILE)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        self.db.commit()

        header = tk.Frame(root, bg="#0c1528", padx=20, pady=15)
        header.pack(fill="x")
        tk.Label(
            header, text="RAED AI", font=("Segoe UI", 23, "bold"),
            bg="#0c1528", fg="#38bdf8"
        ).pack(side="left")
        tk.Label(
            header, text="ASISTENTE PERSONAL",
            font=("Segoe UI", 10), bg="#0c1528", fg="#9fb3c8"
        ).pack(side="right", pady=10)

        self.chat = tk.Text(
            root, bg="#0b1220", fg="#e5eefb",
            insertbackground="white", font=("Segoe UI", 11),
            wrap="word", padx=15, pady=15, relief="flat",
            state="disabled"
        )
        self.chat.pack(fill="both", expand=True, padx=15, pady=(15, 8))

        self.chat.tag_configure("raed", foreground="#38bdf8")
        self.chat.tag_configure("user", foreground="#a5b4fc")

        bottom = tk.Frame(root, bg="#080d18", padx=15, pady=12)
        bottom.pack(fill="x")

        self.entry = tk.Entry(
            bottom, bg="#111c30", fg="white",
            insertbackground="white", font=("Segoe UI", 11),
            relief="flat"
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=12)
        self.entry.bind("<Return>", self.send)

        tk.Button(
            bottom, text="Enviar", command=self.send,
            bg="#0284c7", fg="white", activebackground="#0369a1",
            activeforeground="white", relief="flat",
            font=("Segoe UI", 10, "bold"), padx=20, pady=10
        ).pack(side="left", padx=(8, 0))

        tools = tk.Frame(root, bg="#080d18", padx=15, pady=5)
        tools.pack(fill="x", side="bottom")

        tk.Button(
            tools, text="Ver notas", command=self.show_notes,
            bg="#17243a", fg="#dbeafe", relief="flat"
        ).pack(side="left", padx=(0, 8))
        tk.Button(
            tools, text="Guardar nota", command=self.save_note,
            bg="#17243a", fg="#dbeafe", relief="flat"
        ).pack(side="left")

        self.write("RAED", "Hola. Soy RAED AI, tu asistente personal.\n"
                   "Puedo conversar con comandos básicos, calcular y guardar notas.\n"
                   "Escribe 'ayuda' para ver los comandos disponibles.")
        self.entry.focus_set()
        root.protocol("WM_DELETE_WINDOW", self.close)

    def write(self, sender, text):
        self.chat.configure(state="normal")
        tag = "user" if sender == "Tú" else "raed"
        self.chat.insert("end", f"{sender}: ", tag)
        self.chat.insert("end", text + "\n\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def send(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self.write("Tú", text)
        self.respond(text)

    def respond(self, text):
        low = text.lower().strip()

        if low in ("ayuda", "/ayuda", "help"):
            self.write("RAED", "Comandos disponibles:\n"
                       "• calcula 25 * (8 + 2)\n"
                       "• guardar nota: estudiar Python\n"
                       "• ver notas\n"
                       "• hora\n"
                       "• hola")
        elif low.startswith("calcula "):
            try:
                result = calculate(text[8:].strip())
                self.write("RAED", f"Resultado: {result}")
            except Exception:
                self.write("RAED", "No pude calcularlo. Usa números y "
                           "operaciones como +, -, *, /, %, ** y paréntesis.")
        elif low.startswith("guardar nota:"):
            content = text.split(":", 1)[1].strip()
            if content:
                self.store_note(content)
                self.write("RAED", "Nota guardada en tu PC.")
            else:
                self.write("RAED", "Escribe el contenido después de los dos puntos.")
        elif low in ("ver notas", "/notas"):
            self.show_notes()
        elif low == "hora":
            self.write("RAED", datetime.now().strftime("Hora local: %H:%M:%S | %d/%m/%Y"))
        elif any(word in low for word in ("hola", "buenas", "saludos")):
            self.write("RAED", "¡Hola! ¿En qué trabajamos hoy?")
        elif "quien eres" in low or "quién eres" in low:
            self.write("RAED", "Soy RAED AI. Esta es mi versión inicial; "
                       "todavía no tengo un modelo de lenguaje conectado.")
        else:
            self.write("RAED", "Todavía no sé responder eso. Escribe 'ayuda' "
                       "para ver lo que puedo hacer. Más adelante podremos "
                       "conectarme a un modelo de IA.")

    def store_note(self, content):
        self.db.execute(
            "INSERT INTO notes (created, content) VALUES (?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content)
        )
        self.db.commit()

    def save_note(self):
        content = self.entry.get().strip()
        if not content:
            messagebox.showinfo("RAED AI", "Escribe la nota en el campo de texto primero.")
            return
        self.store_note(content)
        self.entry.delete(0, "end")
        self.write("RAED", "Nota guardada en tu PC.")

    def show_notes(self):
        rows = self.db.execute(
            "SELECT created, content FROM notes ORDER BY id DESC LIMIT 100"
        ).fetchall()
        if not rows:
            self.write("RAED", "Todavía no tienes notas guardadas.")
            return
        self.write("RAED", "Tus notas:\n" + "\n".join(
            f"[{created}] {content}" for created, content in rows
        ))

    def close(self):
        self.db.close()
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    app = RaedAI(window)
    window.mainloop()
