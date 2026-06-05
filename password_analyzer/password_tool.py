import zxcvbn
import argparse
import itertools
import os

# ── 1. PASSWORD ANALYZER ──────────────────────────────────────
def analyze_password(password):
    result = zxcvbn.zxcvbn(password)
    score = result['score']          # 0 (weak) to 4 (strong)
    crack_time = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
    feedback = result['feedback']['suggestions']

    labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    colors = ["red", "orange", "yellow", "blue", "green"]  # for GUI later

    print(f"\n{'='*40}")
    print(f"  Password   : {password}")
    print(f"  Strength   : {labels[score]} ({score}/4)")
    print(f"  Crack Time : {crack_time}")
    if feedback:
        print(f"  Tips       :")
        for tip in feedback:
            print(f"    - {tip}")
    print(f"{'='*40}\n")
    return score

# ── 2. WORDLIST GENERATOR ─────────────────────────────────────
def leetspeak(word):
    replacements = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    result = word
    for char, leet in replacements.items():
        result = result.replace(char, leet).replace(char.upper(), leet)
    return result

def generate_wordlist(name, dob, pet, output_file="wordlist.txt"):
    base_words = [name, dob, pet, name+pet, pet+name]
    years = ["2023", "2024", "2025", "123", "1234", "!"]
    
    wordlist = set()
    for word in base_words:
        if not word:
            continue
        variants = [
            word,
            word.lower(),
            word.upper(),
            word.capitalize(),
            leetspeak(word),
        ]
        for v in variants:
            wordlist.add(v)
            for y in years:
                wordlist.add(v + y)
                wordlist.add(y + v)

    with open(output_file, "w") as f:
        for w in sorted(wordlist):
            f.write(w + "\n")

    print(f"[+] Wordlist saved to '{output_file}' — {len(wordlist)} entries")

# ── 3. CLI INTERFACE ──────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer + Wordlist Generator")
    parser.add_argument("--analyze", type=str, help="Analyze a password")
    parser.add_argument("--generate", action="store_true", help="Generate a custom wordlist")
    parser.add_argument("--output", type=str, default="wordlist.txt", help="Output file name")
    args = parser.parse_args()

    if args.analyze:
        analyze_password(args.analyze)

    if args.generate:
        name = input("Enter name: ")
        dob  = input("Enter date of birth (e.g. 01011999): ")
        pet  = input("Enter pet name: ")
        generate_wordlist(name, dob, pet, args.output)

if __name__ == "__main__":
    main()