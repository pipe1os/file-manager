# Directory Analyzer & Organizer

Just a simple Python script I wrote to practice working with files and the OS module. It helps you clean up messy folders and see where all your hard drive space is going.

## What it does

1. Top 10 Folders: Shows you which folders are taking up the most space. (Uses multithreading now so it won't freeze on massive directories.)
2. Top 10 Files: Finds the biggest individual files (great for hunting down old movies or ISOs you forgot about).
3. Organize: Moves files into categorized folders like `Images/`, `Documents/`, `Audio/` based on their extension.

File types are loaded from `file_types.json`. Gets created automatically on first run if it doesn't exist, so you can edit it to add extensions or rename categories.

## How to run it

You need Python installed. That's it.

```
python file_manager.py
```

Paste the path of the folder you want to analyze when asked. Drag-and-drop into the terminal works too (the script strips out the extra quotes Windows adds automatically).

## Testing

There's a test suite for the collision handling. Needs `pytest`:

```
pip install pytest
pytest test_file_manager.py
```

## Note

Be careful with the "Organize" option because it actually moves your files. If something already exists in the destination it renames the incoming file (`image_1.jpg`, `image_2.jpg`, etc.) so nothing gets overwritten. Still, double-check the path before hitting 'y'. I mostly use it on my downloads folder.
