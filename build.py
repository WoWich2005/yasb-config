import os
import glob
import sass
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = "templates"
OUTPUT_CONFIG = "config.yaml"
OUTPUT_STYLES = "styles.css"

def collect_templates():
    bars = []
    widgets = []

    for bar_file in glob.glob(os.path.join(TEMPLATES_DIR, "bars", "**", "*.yaml.j2"), recursive=True):
        with open(bar_file, encoding="utf-8") as f:
            bars.append(f.read().strip())

    for widget_file in glob.glob(os.path.join(TEMPLATES_DIR, "widgets", "**", "*.yaml.j2"), recursive=True):
        with open(widget_file, encoding="utf-8") as f:
            widgets.append(f.read().strip())

    return bars, widgets

def build_config(bars, widgets):
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("config.yaml.j2")
    rendered = template.render(bars=bars, widgets=widgets)

    with open(OUTPUT_CONFIG, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"✅ config.yaml")

def build_styles():
    scss_parts = []

    for style_file in sorted(glob.glob(os.path.join(TEMPLATES_DIR, "styles", "*.scss"))):
        with open(style_file, encoding="utf-8") as f:
            scss_parts.append(f.read())

    for bar_style in glob.glob(os.path.join(TEMPLATES_DIR, "bars", "**", "*.scss"), recursive=True):
        with open(bar_style, encoding="utf-8") as f:
            scss_parts.append(f.read())

    for widget_style in glob.glob(os.path.join(TEMPLATES_DIR, "widgets", "**", "*.scss"), recursive=True):
        with open(widget_style, encoding="utf-8") as f:
            scss_parts.append(f.read())

    scss_full = "\n".join(scss_parts)
    css = sass.compile(string=scss_full)

    with open(OUTPUT_STYLES, "w", encoding="utf-8") as f:
        f.write(css)

    print(f"✅ styles.css")

if __name__ == "__main__":
    bars, widgets = collect_templates()
    build_config(bars, widgets)
    build_styles()
