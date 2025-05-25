import json
import difflib
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

def load_movies(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def fuzzy_match(user_input, target, threshold=0.6):
    if not user_input:
        return True
    user_input = user_input.lower()
    target = target.lower()

    if user_input in target:
        return True

    ratio = difflib.SequenceMatcher(None, user_input, target).ratio()
    return ratio >= threshold

def recommend_movies(movies, genre, language, director):
    recommendations = []
    for movie in movies:
        if fuzzy_match(genre, movie['genre']) and fuzzy_match(language, movie['language']):
            if director and not fuzzy_match(director, movie['director']):
                continue
            recommendations.append(movie)
    return recommendations

def on_recommend():
    genre = genre_entry.get().strip()
    language = language_entry.get().strip()
    director = director_entry.get().strip()

    # Remove 'not genre' from this check:
    if not language:
        messagebox.showwarning("Input error", "Please enter at least the language.")
        return

    results = recommend_movies(movies, genre, language, director)
    output_box.config(state='normal')
    output_box.delete('1.0', tk.END)

    if results:
        output_box.insert(tk.END, f"Movies that matched your preferences: {len(results)}\n\n")
        for movie in results:
            year = movie.get('year', 'N/A')
            output_box.insert(tk.END, f"- {movie['title']} ({year}) - {movie['genre']} [{movie['language']}]\n")
    else:
        output_box.insert(tk.END, "No matching movies found.")
    output_box.config(state='disabled')


# Load movie data once
movies = load_movies("movies.json")

# Setup Tkinter window
root = tk.Tk()
root.title("Movie Recommender")

root.resizable(False, False)

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky="NSEW")

# Labels and entries
ttk.Label(frame, text="Genre:").grid(row=0, column=0, sticky="W")
genre_entry = ttk.Entry(frame, width=30)
genre_entry.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Language:").grid(row=1, column=0, sticky="W")
language_entry = ttk.Entry(frame, width=30)
language_entry.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Director:").grid(row=2, column=0, sticky="W")
director_entry = ttk.Entry(frame, width=30)
director_entry.grid(row=2, column=1, pady=5)

recommend_btn = ttk.Button(frame, text="Recommend Movies", command=on_recommend)
recommend_btn.grid(row=3, column=0, columnspan=2, pady=10)
root.bind('<Return>', lambda event: on_recommend())

output_box = scrolledtext.ScrolledText(frame, width=60, height=15, state='disabled')
output_box.grid(row=4, column=0, columnspan=2)

def center_window(win):
    win.update_idletasks()

    width = win.winfo_width()
    height = win.winfo_height()

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    win.geometry(f'{width}x{height}+{x}+{y}')

center_window(root)


root.mainloop()
