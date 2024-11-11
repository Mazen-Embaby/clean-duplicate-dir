import os
import pathlib
import shutil


def get_folder_size(folder_path):
    """Calculate the total size of a folder, including all its files."""
    size = 0
    for path in folder_path.rglob('*'):
        if path.is_file():
            try:
                size += path.stat().st_size  # Get the size of each file
            except FileNotFoundError:
                # Handle broken symlinks or files that don't exist
                print(f"Warning: {path} is broken or inaccessible.")
    return size


def process_folder(item_000):
    """Process folders with the '_000' suffix and potentially delete duplicates."""
    f_path = item_000.parent / item_000.name.removesuffix("_000")

    # Get the size of the folder without the '_000' suffix
    f_size = get_folder_size(f_path)

    # Log the sizes and paths
    print(f"Processing Folder: {f_path}")
    print(f"  - Size (without _000): {f_size} bytes")
    print(f"  - _000 Folder: {item_000.absolute()}")

    if f_size == 0:
        # Folder size is 0, so attempt to delete the non-_000 folder
        if f_path.exists():
            try:
                f_path.rmdir()  # Remove the empty folder
                print(f"  - Folder {f_path} removed (empty).")
            except OSError as e:
                print(f"  - Error removing folder {f_path}: {e}")
        else:
            print(f"  - Folder {f_path} does not exist.")

        # Rename the '_000' folder to the folder name without '_000'
        try:
            item_000.rename(f_path)
            print(f"  - Renamed {item_000} to {f_path}")
        except Exception as e:
            print(f"  - Error renaming {item_000}: {e}")
    else:
        print("  - Folder size > 0, no action taken.")


def process_file(item_000):
    """Process files with the '_000' suffix and delete if they match the original."""
    f_path = item_000.parent / item_000.name.replace("_000", '')

    if f_path.exists():
        f_size = f_path.stat().st_size
        f_000_size = item_000.stat().st_size

        print(f"Processing File: {f_path}")
        print(f"  - Size (without _000): {f_size} bytes")
        print(f"  - _000 File: {item_000.absolute()} (Size: {f_000_size} bytes)")

        if f_size == f_000_size:
            try:
                item_000.unlink()  # Delete the '_000' file
                print(f"  - Deleted {item_000}")
            except Exception as e:
                print(f"  - Error deleting {item_000}: {e}")
    else:
        print(f"  - Original file {f_path} not found. Skipping.")


def main():
    rootdir = '/mnt/XXXX/'

    # Pathlib handles cross-platform file paths more easily than os.path
    path_lib = pathlib.Path(rootdir)

    # Find all items that match the '_000' pattern
    rec_items = path_lib.rglob("*_000*")

    for item_000 in rec_items:
        if item_000.is_dir():
            process_folder(item_000)
        elif item_000.is_file():
            process_file(item_000)
        else:
            print(f"Unknown item type: {item_000}")

    print("Processing complete.")


if __name__ == '__main__':
    main()
