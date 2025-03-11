import pytest
import os
import tempfile
from app.models.animal import Animal
from app.html_generator import HTMLGenerator


class TestHTMLGenerator:
    def test_html_generator(self, monkeypatch):
        # Create a temporary file to use as the output HTML file.
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            temp_output = tmp_file.name

        # Prepare a list of dummy animals.
        animals = [
            Animal(name="Animal1", collateral_adjective="adj1", image_path="/path/to/image1.jpg"),
            Animal(name="Animal2", collateral_adjective="adj2", image_path=None),
        ]

        # Generate the HTML output.
        html_gen = HTMLGenerator(output_file_name=temp_output)
        html_gen.generate_html(animals)

        # Read and check the output file contents.
        with open(temp_output, "r", encoding="utf-8") as f:
            content = f.read()

        assert "Animal1 (adj1)" in content
        assert "Picture" in content
        assert "Animal2 (adj2)" in content
        assert "No image" in content

        # Cleanup: remove the temporary output file.
        os.remove(temp_output)
