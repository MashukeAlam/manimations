"""
Generate scripts using following Prompt

Given a programming topic, generate a JSON script to teach that topic via video tutorial.
The JSON must follow this exact format:

{
  "intro": "<brief engaging introduction>",
  "sections": [
    {
      "type": "code",
      "code_string": "<code snippet>",
      "annotation": "<short description of what the snippet does>",
      "highlight_lines": [<line numbers to highlight>],
      "explanation": "<detailed explanation of the code and logic>"
    },
    {
      "type": "quiz",
      "question": "<short quiz question about the topic or previous code>",
      "answer": "<concise answer to the quiz question>"
    }
    // Add as many sections as needed, mixing code and quiz sections
  ],
  "outro": "<friendly closing line encouraging the learner>"
}

Requirements:

Use valid JSON syntax.
Use double quotes for all keys and strings.
Escape any characters properly (like \n in code).
Keep each code_string limited to 5–10 lines (write comments if needed).
Add 10 to 14 sections for depth.
Keep intro, outro, explanations, annotations, questions, and answers concise (between 5–7 words).
Alternate or mix code and quiz sections for engagement.

"""


from manim import *
import json
import os
from generate_voice import generate_voice_and_get_duration


class Video(Scene):
    def __init__(self, **kwargs):
        # Get the script file path from the environment variable
        json_path = os.environ.get("MANIM_SCRIPT_FILE", "test.json")
        super().__init__(**kwargs)
        with open(json_path, "r") as f:
            self.tutorial_data = json.load(f)

    def construct(self):
        self.show_intro(self.tutorial_data.get("intro", ""))
        sections = self.tutorial_data.get("sections", [])
        for section in sections:
            section_type = section.get("type", "code")
            if section_type == "quiz":
                self.show_quiz_section(section)
            elif section_type == "real_world":
                self.show_real_world_section(section)
            else:
                self.show_code_section(section)
            # Animated transition between sections
            self.animate_section_transition()
        self.show_outro(self.tutorial_data.get("outro", ""))
        # self.show_outro("Thank you for watching! Consider subscribing to the channel.")

    def show_intro(self, text):
        if not text:
            return
        intro = Text(text, font_size=24)
        self.play(Write(intro))
        self.wait(1)
        self.play(intro.animate.to_edge(UP))

    def show_code_section(self, section):
        code_string = section.get("code_string", "")
        annotation = section.get("annotation", "")
        explanation = section.get("explanation", "")

        # Generate voiceover and get duration
        audio_file, audio_duration = generate_voice_and_get_duration(explanation)

        # Code block
        code = Code(
            code_string=code_string,
            language="python",
            formatter_style="monokai",
            background="window",
            add_line_numbers=True,
            background_config={
                "buff": 0.3,
                "fill_color": ManimColor("#222"),
                "stroke_color": MAROON_A,
                "corner_radius": 0.3,
                "stroke_width": 1,
                "fill_opacity": 1,
            },
            paragraph_config={
                "font": "CaskaydiaMono Nerd Font Mono",
                "font_size": 24,
                "line_spacing": 0.5,
                "disable_ligatures": True,
            },
        )

        self.play(FadeIn(code, shift=UP))
        self.wait(0.7)

        elements = [code]

        # Annotation text (usually below)
        if annotation:
            annotation_text = Paragraph(annotation, font_size=32).next_to(code, DOWN)
            self.play(FadeIn(annotation_text))
            self.wait(1)
            elements.append(annotation_text)

        # Explanation text and audio
        if explanation:
            explanation_text = Paragraph(
                explanation, font_size=24, slant=ITALIC, line_spacing=0.5
            )
            explanation_text.next_to(code, DOWN, buff=1.5)
            explanation_text.scale_to_fit_width(config.frame_width - 1)

            if audio_file:
                self.add_sound(audio_file)

            self.play(Write(explanation_text))
            self.wait(audio_duration + 3)
            elements.append(explanation_text)

        # Fade everything out
        self.play(FadeOut(Group(*elements)))

    def show_outro(self, text):
        if not text:
            return
        outro = Paragraph(text, font_size=24)
        outro.scale_to_fit_width(config.frame_width - 1)
        self.play(Write(outro))
        self.wait(2)

    def animate_section_transition(self):
        # Simple fade to black and back in
        fade_rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0,
        )
        self.play(FadeIn(fade_rect, run_time=0.5))
        self.wait(0.2)
        self.play(FadeOut(fade_rect, run_time=0.5))

    def show_quiz_section(self, section):
        question = section.get("question", "")
        answer = section.get("answer", "")
        if not question or not answer:
            return
        # Generate voiceover for question and answer
        q_audio, q_duration = generate_voice_and_get_duration(f"Please try to answer this question - {question}")
        a_audio, a_duration = generate_voice_and_get_duration(f"Answer should be - {answer}")
        q_text = Paragraph(f"Quiz: {question}", font_size=32)
        self.play(Write(q_text))
        if q_audio:
            self.add_sound(q_audio)
        self.wait(q_duration + 3)
        a_text = (
            Paragraph(f"Answer: {answer}", font_size=28, color=GREEN)
            .next_to(q_text, DOWN)
        )
        self.play(Write(a_text))
        if a_audio:
            self.add_sound(a_audio)
        self.wait(a_duration + 1)
        self.play(FadeOut(Group(q_text, a_text)))

    def show_real_world_section(self, section):
        desc = section.get("description", "")
        code = section.get("code_string", "")
        elements = []
        if desc:
            desc_text = Paragraph(desc, font_size=28)
            self.play(Write(desc_text))
            self.wait(1)
            elements.append(desc_text)
        if code:
            code_block = Code(
                code_string=code,
                language="python",
                formatter_style="monokai",
                background="window",
                add_line_numbers=True,
                background_config={
                    "buff": 0.3,
                    "fill_color": ManimColor("#222"),
                    "stroke_color": MAROON_A,
                    "corner_radius": 0.3,
                    "stroke_width": 1,
                    "fill_opacity": 1,
                },
                paragraph_config={
                    "font": "CaskaydiaMono Nerd Font Mono",
                    "font_size": 24,
                    "line_spacing": 0.5,
                    "disable_ligatures": True,
                },
            )
            self.play(FadeIn(code_block, shift=UP))
            self.wait(2)
            elements.append(code_block)
        if elements:
            self.play(FadeOut(Group(*elements)))

