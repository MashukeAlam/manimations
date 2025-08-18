# Manimations

## Overview
**Manimations** is an automated video tutorial generator for programming topics. It uses Manim to create engaging, narrated videos from structured JSON scripts, supporting code explanations, quizzes, and real-world examples.

---

## Features
- **Script-driven video generation** using JSON
- **Code, quiz, and real-world sections** with voiceover
- **Animated transitions** and code highlighting
- **Automatic voiceover** using TTS
- **MCP server integration** for Claude AI
- **Shorts generator** with NASA APOD backgrounds
- **Batch processing** for multiple scripts

---

## Getting Started

### 1. Install Dependencies (using uv)

```sh
uv sync
```

### 2. Usage Options

#### Option A: Single Video Generation
- Place your JSON script in `test.json`
- Run:
```sh
uv run main.py
```

#### Option B: MCP Server (for Claude AI)
- Use the MCP server (VS Code or Claude AI can take advantage of these two MCPs):
```sh
run_mcp.py  & save_json.py
```
- Connect to Claude AI to generate scripts and videos automatically

#### Option C: Batch Processing
- Place multiple JSON scripts in your 'scritps' directory
- Run:
```sh
uv run wrapper.py
```
- This will process all scripts one after another

### 3. Generate Shorts
- Place your quotes in `generated_shorts/quotes.json`
- Place a background audio file... **this feature is not tested**
- Run:
```sh
uv run shorts.py
```
- The script will fetch NASA images and create short videos

---

## JSON Script Format

Your script should follow this structure (see `main.py` docstring for details):

```json
{
  "intro": "Brief engaging introduction",
  "sections": [
    {
      "type": "code",
      "code_string": "print('Hello World')",
      "annotation": "Basic print statement",
      "highlight_lines": [1],
      "explanation": "This prints text to console"
    },
    {
      "type": "quiz",
      "question": "What does print() do?",
      "answer": "Displays text output"
    }
  ],
  "outro": "Great job learning!"
}
```

---

## File Structure

- `main.py` - Core video generation engine
- `run_mcp.py` - MCP server for Claude AI integration
- `wrapper.py` - Batch processor for multiple scripts
- `shorts.py` - Short video generator with NASA backgrounds
- `generate_voice.py` - Text-to-speech functionality
- `cleanup.py` - Log file management

---

## Customization

- **Edit `main.py`** to change video style or add new section types
- **Edit `generate_voice.py`** to change TTS voice or language
- **Edit NASA API key** in `shorts.py` for background images

---

## Tips

- For best results, use concise explanations and quiz questions (5-7 words)
- You can add your own images, voices, or code styles
- Use `wrapper.py` for processing multiple tutorial scripts efficiently

---

## License

MIT License

---

*If you have questions or want to contribute, open an issue or pull request!*