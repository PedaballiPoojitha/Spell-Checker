class SpellChecker:
    def __init__(self):
        self.dictionary = set()

    def load_dictionary(self, words):
        self.dictionary.update(word.lower() for word in words)

    def levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        prev = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            curr = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = prev[j + 1] + 1
                deletions = curr[j] + 1
                substitutions = prev[j] + (c1 != c2)
                curr.append(min(insertions, deletions, substitutions))
                prev = curr

                return prev[-1]

    def is_correct(self, word):
        return word.lower() in self.dictionary

    def suggest_corrections(self, word, max_distance=2, top_k=5):
        word_lower = word.lower()
        if word_lower in self.dictionary:
            return [word]

        suggestions = []
        for dict_word in self.dictionary:
            distance = self.levenshtein_distance(word_lower, dict_word)
            if distance <= max_distance:
                suggestions.append((distance, dict_word))

                suggestions.sort()
                return [word for _, word in suggestions[:top_k]]

    def context_rank(self, word, context_words):
        suggestions = self.suggest_corrections(word)
        if not suggestions:
            return []

        context_avg_len = sum(len(w) for w in context_words) / len(context_words) if context_words else 0
        ranked = sorted(suggestions, key=lambda w: abs(len(w) - context_avg_len))
        return ranked

if __name__ == "__main__":
    print("\n=== SPELL CHECKER ===")
    checker = SpellChecker()

    # Load default dictionary
    default_words = ["hello", "world", "python", "programming", "spell", "checker",
    "computer", "science", "algorithm", "data", "structure"]
    checker.load_dictionary(default_words)
    print(f"Loaded {len(default_words)} words into dictionary")

    while True:
        print("\n" + "="*40)
        print("1. Check Word")
        print("2. Get Suggestions")
        print("3. Add Word to Dictionary")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            word = input("Enter word to check: ")
            if checker.is_correct(word):
                print(f"✓ '{word}' is spelled correctly")
            else:
                print(f"✗ '{word}' is misspelled")
                suggestions = checker.suggest_corrections(word)
                if suggestions:
                    print(f"Suggestions: {suggestions}")
                elif choice == '2':
                    word = input("Enter word: ")
                    suggestions = checker.suggest_corrections(word)
                    if suggestions:
                        print(f"Suggestions: {suggestions}")
                    else:
                        print("No suggestions found")
                elif choice == '3':
                    word = input("Enter word to add: ")
                    checker.dictionary.add(word.lower())
                    print(f"✓ Added '{word}' to dictionary")
                elif choice == '4':
                    break