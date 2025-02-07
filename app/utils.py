import os

def create_file_and_directories_if_not_exist(filepath):
    """Creates a file and any necessary parent directories.

    Args:
      filepath: The path to the file.
    """
    if not os.path.exists(filepath):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True) # Create dirs if needed
            with open(filepath, "w") as f:  # 'w' mode creates the file
                print(f"File '{filepath}' created successfully.")
        except Exception as e:
            print(f"Error creating file '{filepath}': {e}")
    else:
        print(f"File '{filepath}' already exists.")
