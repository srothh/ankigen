#!/usr/bin/env python3
"""
create_anki_deck.py

This script reads a text file containing a Python-style list of 5-tuples.
Each tuple must have the form:
    (hanzi, pinyin, english, german, sentence)

For example, the contents of input.txt might look like:

[
    ('男', 'nán', 'man', 'Mann', '他是一个男人。'),
    ('学', 'xué', 'to study', 'lernen', '我喜欢学习中文。'),
    # ... more tuples ...
]

The script uses the genanki library to generate an Anki deck (.apkg) where:
- The front of each card shows the Chinese character (hanzi), centered and in large font.
- The back of each card shows:
    • The front side again (so it stays visible after clicking “Show Answer”)
    • Pinyin
    • English translation
    • German translation
    • Example sentence (in Chinese)

Usage:
    python create_anki_deck.py input.txt output.apkg

If no output file is specified, it defaults to "deck.apkg".

Dependencies:
    • genanki (install via pip: pip install genanki)
"""

import sys
import os
import ast
import genanki

def load_tuples_from_file(filename):
    """
    Reads a text file and parses it as a Python literal to extract a list of 5-tuples.
    Uses ast.literal_eval for safety (no arbitrary code execution).
    Each tuple is expected to have exactly 5 elements:
        (hanzi, pinyin, english, german, sentence)
    Returns:
        A list of tuples.
    """
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' does not exist.")
        sys.exit(1)

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        data = ast.literal_eval(content)
    except Exception as e:
        print(f"Error parsing '{filename}': {e}")
        sys.exit(1)

    if not isinstance(data, list):
        print(f"Error: Expected a list of tuples in '{filename}'.")
        sys.exit(1)

    # Validate each entry
    for idx, entry in enumerate(data):
        if not (isinstance(entry, tuple) and len(entry) == 5):
            print(f"Error: Entry {idx} in '{filename}' is not a 5-tuple: {entry}")
            sys.exit(1)

    return data

def create_anki_deck(tuples_list, deck_name="Chinese Vocabulary", deck_id=2059400110, model_id=1607392319):
    """
    Creates an Anki deck from a list of 5-tuples:
        (hanzi, pinyin, english, german, sentence)

    Parameters:
        tuples_list: List of 5-tuples.
        deck_name: Name of the deck (string).
        deck_id: A unique integer ID for the deck.
        model_id: A unique integer ID for the note type (model).
    Returns:
        genanki.Deck object populated with cards.
    """

    chinese_model = genanki.Model(
        model_id,
        'ChineseCharacterModel',
        fields=[
            {'name': 'Hanzi'},
            {'name': 'Pinyin'},
            {'name': 'English'},
            {'name': 'German'},
            {'name': 'Sentence'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': """
                <div style="display:flex; justify-content:center; align-items:center; height:100%;">
                  <span style="font-size: 72px; font-family: Arial, sans-serif;">{{Hanzi}}</span>
                </div>
                """,
                'afmt': """
                {{FrontSide}}
                <hr id="answer-divider">
                <div style="text-align:center; margin-top: 20px;">
                  <div style="font-size: 24px; font-family: Arial, sans-serif; margin-bottom: 10px;">
                    <strong>Pinyin:</strong> {{Pinyin}}
                  </div>
                  <div style="font-size: 24px; font-family: Arial, sans-serif; margin-bottom: 10px;">
                    <strong>English:</strong> {{English}}
                  </div>
                  <div style="font-size: 24px; font-family: Arial, sans-serif; margin-bottom: 10px;">
                    <strong>German:</strong> {{German}}
                  </div>
                  <div style="font-size: 24px; font-family: Arial, sans-serif; margin-top: 10px;">
                    <strong>Example:</strong> {{Sentence}}
                  </div>
                </div>
                """,
            },
        ],
        css="""
        .card {
          text-align: center;
          font-family: Arial, sans-serif;
          background-color: #ffffff;
          color: #000000;
        }

        #answer-divider {
          margin-top: 20px;
          margin-bottom: 20px;
          border: none;
          border-top: 1px solid #cccccc;
        }
        """
    )

    # Create the deck and add notes/cards
    deck = genanki.Deck(deck_id, deck_name)

    for entry in tuples_list:
        hanzi, pinyin, english, german, sentence = entry

        note = genanki.Note(
            model=chinese_model,
            fields=[hanzi, pinyin, english, german, sentence]
        )
        deck.add_note(note)

    return deck

def main():

    input_file = sys.argv[1] if len(sys.argv) >= 2 else "input.txt"
    output_file = sys.argv[2] if len(sys.argv) >= 3 else "textlekt2a.apkg"

    tuples_list = load_tuples_from_file(input_file)

    deck = create_anki_deck(tuples_list)

    try:
        genanki.Package(deck).write_to_file(output_file)
        print(f"Anki deck successfully created: {output_file}")
    except Exception as e:
        print(f"Error writing Anki deck to '{output_file}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
