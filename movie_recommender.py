import json
import difflib

def load_movies(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_user_preferences():
    genre = input("Enter preferred genre (e.g. Sci-Fi, Drama): ").strip()
    language = input("Enter preferred language:").strip()
    director = input("Enter preferred director:").strip()
    return genre, language, director

def fuzzy_match(user_input, target, threshold=0.6):
    if not user_input:
        return True  # empty input matches anything
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

def main():
    movies = load_movies("movies.json")
    genre, language, director = get_user_preferences()

    # Optional: check if language is entered; or you can skip this if you want it fully optional
    if not language:
        print("Please enter at least a language.")
        return

    results = recommend_movies(movies, genre, language, director)

    if results:
        print(f"Movies that matched your preferences: {len(results)}")
        for movie in results:
            year = movie.get('year', 'N/A')
            print(f"- {movie['title']} ({year}) - {movie['genre']} [{movie['language']}]")
    else:
        print("No matching movies found.")

if __name__ == "__main__":
    main()
