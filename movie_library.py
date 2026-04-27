import json
import os
from tkinter import *
from tkinter import ttk, messagebox

DATA_FILE = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("850x500")
        self.root.resizable(True, True)

        self.movies = []
        self.load_data()

        self.filter_genre = StringVar(value="Все")
        self.filter_year = StringVar(value="")

        self.create_widgets()
        self.refresh_table()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except:
                self.movies = []
        else:
            self.movies = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def validate_input(self, title, genre, year_str, rating_str):
        if not title.strip():
            messagebox.showerror("Ошибка", "Название не может быть пустым")
            return False
        if not genre.strip():
            messagebox.showerror("Ошибка", "Жанр не может быть пустым")
            return False
        try:
            year = int(year_str)
            if year < 1888 or year > 2100:
                messagebox.showerror("Ошибка", "Год должен быть от 1888 до 2100")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть целым числом")
            return False
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом")
            return False
        return True

    def add_movie(self):
        title = self.entry_title.get()
        genre = self.entry_genre.get()
        year = self.entry_year.get()
        rating = self.entry_rating.get()

        if self.validate_input(title, genre, year, rating):
            movie = {
                "title": title.strip(),
                "genre": genre.strip(),
                "year": int(year),
                "rating": float(rating)
            }
            self.movies.append(movie)
            self.save_data()
            self.refresh_table()
            self.entry_title.delete(0, END)
            self.entry_genre.delete(0, END)
            self.entry_year.delete(0, END)
            self.entry_rating.delete(0, END)
            self.update_genre_filter()

    def get_filtered_movies(self):
        genre = self.filter_genre.get()
        year_str = self.filter_year.get().strip()
        filtered = self.movies[:]
        if genre != "Все":
            filtered = [m for m in filtered if m["genre"].lower() == genre.lower()]
        if year_str:
            try:
                year_int = int(year_str)
                filtered = [m for m in filtered if m["year"] == year_int]
            except ValueError:
                pass
        return filtered

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for movie in self.get_filtered_movies():
            self.tree.insert("", END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def update_genre_filter(self):
        genres = sorted(set(m["genre"] for m in self.movies))
        current = self.filter_genre.get()
        self.genre_filter_menu['values'] = ["Все"] + genres
        if current not in self.genre_filter_menu['values']:
            self.filter_genre.set("Все")

    def reset_filters(self):
        self.filter_genre.set("Все")
        self.filter_year.set("")
        self.refresh_table()

    def create_widgets(self):
10:04
input_frame = LabelFrame(self.root, text="Добавить новый фильм", padx=10, pady=10)
        input_frame.pack(fill=X, padx=10, pady=5)

        Label(input_frame, text="Название:").grid(row=0, column=0, sticky=W, padx=5, pady=2)
        self.entry_title = Entry(input_frame, width=30)
        self.entry_title.grid(row=0, column=1, padx=5, pady=2)

        Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky=W, padx=5, pady=2)
        self.entry_genre = Entry(input_frame, width=20)
        self.entry_genre.grid(row=0, column=3, padx=5, pady=2)

        Label(input_frame, text="Год выпуска:").grid(row=1, column=0, sticky=W, padx=5, pady=2)
        self.entry_year = Entry(input_frame, width=10)
        self.entry_year.grid(row=1, column=1, sticky=W, padx=5, pady=2)

        Label(input_frame, text="Рейтинг (0–10):").grid(row=1, column=2, sticky=W, padx=5, pady=2)
        self.entry_rating = Entry(input_frame, width=10)
        self.entry_rating.grid(row=1, column=3, sticky=W, padx=5, pady=2)

        btn_add = Button(input_frame, text="Добавить фильм", command=self.add_movie, bg="#4CAF50", fg="white")
        btn_add.grid(row=0, column=4, rowspan=2, padx=15, pady=5)

        filter_frame = LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill=X, padx=10, pady=5)

        Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=5)
        self.genre_filter_menu = ttk.Combobox(filter_frame, textvariable=self.filter_genre, state="readonly", width=20)
        self.genre_filter_menu.grid(row=0, column=1, padx=5)
        self.update_genre_filter()
        self.genre_filter_menu.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        Label(filter_frame, text="Год выпуска:").grid(row=0, column=2, padx=5)
        self.year_filter_entry = Entry(filter_frame, textvariable=self.filter_year, width=10)
        self.year_filter_entry.grid(row=0, column=3, padx=5)
        self.year_filter_entry.bind("<KeyRelease>", lambda e: self.refresh_table())

        btn_reset = Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters)
        btn_reset.grid(row=0, column=4, padx=15)

        table_frame = Frame(self.root)
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        self.tree.column("Название", width=300)
        self.tree.column("Жанр", width=150)
        self.tree.column("Год", width=80)
        self.tree.column("Рейтинг", width=80)
        self.tree.pack(fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

if __name__ == "__main__":
    root = Tk()
    app = MovieLibrary(root)
    root.mainloop()
