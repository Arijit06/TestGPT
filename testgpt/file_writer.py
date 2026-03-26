# testgpt/file_writer.py

from pathlib import Path


def save_test_file(class_name: str, code: str, output_dir: str = "generated_tests") -> Path:
    """
    Saves generated Java code to a .java file.
    Creates the output directory if it doesn't exist.
    Returns the path to the saved file.
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / f"{class_name}.java"
    file_path.write_text(code)

    return file_path