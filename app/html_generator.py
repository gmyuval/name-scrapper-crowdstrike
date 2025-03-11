from pathlib import Path
from app.models.animal import Animal
from app.config import HTML_HEADER, HTML_FOOTER, OUTPUT_HTML_FILE_NAME, OUTPUT_DIR


class HTMLGenerator:
    MISSING_IMAGE_TEXT = "No image"

    def __init__(
        self,
        html_header: str = HTML_HEADER,
        html_footer: str = HTML_FOOTER,
        output_dir: str = OUTPUT_DIR,
        output_file_name: str = OUTPUT_HTML_FILE_NAME,
    ) -> None:
        self.html_header = html_header
        self.html_footer = html_footer
        self.output_dir = output_dir
        self.output_file_name = output_file_name

    def generate_html(self, animals: list[Animal]) -> None:
        html_content = self.html_header
        for animal in animals:
            image_link = f"<a href='{animal.image_path}'>Picture</a>" if animal.image_path else self.MISSING_IMAGE_TEXT
            html_content += f"<li>{animal.name} ({animal.collateral_adjective}) - {image_link}</li>"
        html_content += self.html_footer
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        output_file = Path.joinpath(Path(self.output_dir), self.output_file_name)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Output written to {output_file}")
