import hashlib
import os

from constants import PHOTOS_EXT

# Не очень хорошо работает код. Ищет по названию и метаданным. Чисто по содержимому дупы не ищет.


def calculate_file_hash(filepath, hash_algorithm='sha256'):
    """Calculate the hash of a file using the specified hash algorithm."""
    hash_func = hashlib.new(hash_algorithm)
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def find_duplicate_photos(directory):
    """Find and return a dictionary of duplicate photo files in the given directory."""
    hash_to_files = {}
    duplicates = {}

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                # Process only image files (extensions can be extended as needed)
                # ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
                if file.lower().endswith(tuple(PHOTOS_EXT)):
                    file_hash = calculate_file_hash(filepath)
                    if file_hash in hash_to_files:
                        duplicates.setdefault(file_hash, []).append(filepath)
                    else:
                        hash_to_files[file_hash] = filepath
            except Exception as e:
                print(f"Error processing file {filepath}: {e}")

    # Combine original files with their duplicates
    return {hash_: [hash_to_files[hash_]] + paths for hash_, paths in duplicates.items() if len(paths) > 1}


def save_duplicates_to_file(duplicates, output_file):
    """Save the duplicates dictionary to a text file."""
    with open(output_file, 'w') as f:
        for original_and_duplicates in duplicates.values():
            f.write(f"Original: {original_and_duplicates[0]}\n")
            for duplicate in original_and_duplicates[1:]:
                f.write(f"  Duplicate: {duplicate}\n")
            f.write("\n\n")


if __name__ == "__main__":
    directory_to_scan = input("Enter the directory path to scan for duplicate photos: ")
    output_file = input("Enter the output file path to save results: ")

    if not os.path.isdir(directory_to_scan):
        print("The specified directory does not exist.")
    else:
        duplicates = find_duplicate_photos(directory_to_scan)
        if duplicates:
            save_duplicates_to_file(duplicates, output_file)
            print(f"Duplicate photos found and saved to {output_file}.")
        else:
            print("No duplicate photos found.")
