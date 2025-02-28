import os
import re
import htmlmin
from fastapi.responses import HTMLResponse


def create_file_and_directories_if_not_exist(filepath):
    """Creates a file and any necessary parent directories.

    Args:
      filepath: The path to the file.
    """
    if not os.path.exists(filepath):
        try:
            os.makedirs(
                os.path.dirname(filepath), exist_ok=True
            )  # Create dirs if needed
            with open(filepath, "w") as f:  # 'w' mode creates the file
                print(f"File '{filepath}' created successfully.")
        except Exception as e:
            print(f"Error creating file '{filepath}': {e}")
    else:
        print(f"File '{filepath}' already exists.")


async def minify_html(request):
    """Minifies HTML responses."""
    # return request
    if request.media_type == "text/html":  # Check if it's an HTML response
        response = request
        try:
            content = request.body  # Read the response body
            minified_content = htmlmin.minify(
                content.decode("utf-8"),
                remove_empty_space=True,
                remove_all_empty_space=True,
            )  # Minify the HTML
            response = HTMLResponse(
                minified_content, status_code=request.status_code
            )  # Create a new response
        except Exception as e:
            print(f"Error minifying HTML: {e}")  # Handle potential errors (important!)
        return response


def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def convert_bytes(size_in_bytes, unit="auto"):
    """
    Mengonversi ukuran dalam byte ke satuan lain (B, KB, MB, GB, TB, PB).

    :param size_in_bytes: Jumlah byte (int)
    :param unit: Satuan tujuan ("B", "KB", "MB", "GB", "TB", "PB", atau "auto" untuk otomatis).
    :return: Nilai dalam satuan yang dipilih (float) dengan 2 desimal.
    """
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    factor = 1024  # 1 KB = 1024 B

    if unit == "auto":
        index = 0
        while size_in_bytes >= factor and index < len(units) - 1:
            size_in_bytes /= factor
            index += 1
        return f"{size_in_bytes:.2f} {units[index]}"

    if unit in units:
        index = units.index(unit)
        converted_size = size_in_bytes / (factor**index)
        return f"{converted_size:.2f} {unit}"

    raise ValueError(
        "Unit tidak valid. Gunakan 'B', 'KB', 'MB', 'GB', 'TB', atau 'PB'."
    )


def convert_bytes_to_mb(bytes):
    mb = bytes / (1024 * 1024)
    return mb
