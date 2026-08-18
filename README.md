# LyricScript

A domain-specific language (DSL) for writing and structuring songs.

## What is it?

LyricScript is a lightweight language designed specifically for songwriters. Instead of scattered notes, your lyrics live in clean structured files with defined sections, ordering, and commands.

## Quick Example

Write this in a `.lsc` file:
```
song "Distance"

structure {
  verse1 -> hook -> verse2 -> hook
}

verse1 {
  "You're 300 miles away"
  "It feel like forever"
}

hook {
  "Slide, slide"
  repeat 3
}

verse2 {
  "Phone light hitting your face"
}
```

Run it:
```
python main.py distance.lsc
```

Get this:
```
Distance

========================================

  [VERSE1]
    You're 300 miles away
    It feel like forever

  [HOOK]
    Slide, slide
    Slide, slide
    Slide, slide

  [VERSE2]
    Phone light hitting your face

  [HOOK]
    Slide, slide
    Slide, slide
    Slide, slide

========================================
```
## Web Editor

LyricScript also runs in the browser. Start the server:
Then open `http://127.0.0.1:5000/`. Write LyricScript on the left, hit Run, and the formatted song appears on the right. Export saves the output to a file.

## Language Reference

| Syntax | What it does |
|---|---|
| `song "Title"` | Defines the song name |
| `structure { a -> b -> c }` | Sets the order sections play in |
| `sectionname { }` | Defines a section (verse, hook, bridge, etc.) |
| `"lyric line"` | A line of lyrics inside a section |
| `repeat N` | Repeats the previous line N times |
| `% comment` | A comment, ignored by the language |

## How it Works

LyricScript is built as a full compiler pipeline:

1. **Tokenizer** — reads raw `.lsc` text and labels every piece (keywords, strings, numbers, symbols)
2. **Parser** — takes those tokens and builds a structured tree, enforcing grammar rules and throwing errors with line numbers if something is wrong
3. **Interpreter** — walks that tree and produces formatted output

## Requirements

- Python 3.x
- Flask (only needed for the web editor; the CLI runs on the standard library alone)

```
pip install flask
```

## Usage
```
python main.py <file.lsc>
```

## Project Structure
```
LyricScript/
├── main.py          # CLI entry point
├── server.py        # Flask web server
├── tokenizer.py     # lexical analysis
├── parser.py        # syntax analysis
├── interpreter.py   # output generation
├── templates/
│   └── index.html   # browser editor UI
└── distance.lsc     # example song
```

```
