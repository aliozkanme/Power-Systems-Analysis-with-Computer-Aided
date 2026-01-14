import os
import re

# --- CONFIGURATION ---
# The target Markdown file to update in-place.
TARGET_FILE = "README.md"

# Directory where source code files are stored.
SOURCE_DIR = "src"

# Map file extensions to Markdown syntax highlighting tags.
EXT_MAP = {
    ".py": "python",
    ".m": "matlab",
    ".js": "javascript",
    ".c": "c",
    ".cpp": "cpp",
    ".java": "java",
    ".html": "html",
    ".css": "css",
    ".sh": "bash",
    ".json": "json",
    ".xml": "xml",
    ".md": "markdown"
}

def get_language_tag(filepath):
    """
    Determines the Markdown language tag based on the file extension.
    """
    _, ext = os.path.splitext(filepath)
    return EXT_MAP.get(ext.lower(), "")

def read_source_file(filename):
    """
    Reads content from the source file in SOURCE_DIR.
    Returns the content or an error message string.
    """
    file_path = os.path.join(SOURCE_DIR, filename)
    
    if not os.path.exists(file_path):
        print(f"[WARNING] Source file not found: {file_path}")
        return f"> **ERROR:** File '{filename}' not found."
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"[ERROR] Could not read {file_path}: {e}")
        return f"> **ERROR:** Read permission failed for '{filename}'."

def main():
    """
    Main execution:
    1. Reads the TARGET_FILE line by line.
    2. Detects '[](filename)' markers.
    3. Inserts/Updates the code block immediately after the marker.
    4. Skips any existing code block under the marker to avoid duplication.
    """
    if not os.path.exists(TARGET_FILE):
        print(f"[FATAL] Target file '{TARGET_FILE}' not found.")
        return

    print(f"--- Updating {TARGET_FILE} ---")

    # Read all lines from the target file
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    # Regex to find the invisible link marker: [](filename.ext)
    # The filename is captured in group 1
    marker_pattern = re.compile(r"^\s*\[\]\((.*?)\)\s*$")

    while i < len(lines):
        line = lines[i]
        match = marker_pattern.search(line)

        if match:
            # Found a marker like [](code.py)
            filename = match.group(1).strip()
            print(f"[INFO] Found marker for: {filename}")

            # 1. Append the marker line itself (so it stays in the file)
            new_lines.append(line)

            # 2. Prepare the new code block
            code_content = read_source_file(filename)
            lang_tag = get_language_tag(filename)
            
            # Create the formatted code block
            new_block = f"```{lang_tag}\n{code_content}\n```\n"
            new_lines.append(new_block)

            # 3. Check if there is an OLD code block immediately following this marker
            #    We need to skip the old block so we don't duplicate it.
            next_idx = i + 1
            if next_idx < len(lines) and lines[next_idx].strip().startswith("```"):
                # An existing code block starts here. We must skip lines until the closing ```
                print(f"       -> Replacing existing code block for {filename}")
                i += 2 # Skip the current marker line and the opening ```
                
                # Loop to skip content until closing ``` is found
                while i < len(lines):
                    if lines[i].strip().startswith("```"):
                        # Found the closing tag of the old block
                        i += 1 # Move past the closing tag
                        break
                    i += 1
                
                # Continue the main loop from the new position
                continue
            else:
                # No existing code block found, just insert the new one
                print(f"       -> Inserting new code block for {filename}")
                i += 1
        else:
            # Regular line, just keep it
            new_lines.append(line)
            i += 1

    # Write the updated content back to the same file
    try:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print("[SUCCESS] File updated successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to write to {TARGET_FILE}: {e}")

if __name__ == "__main__":
    main()