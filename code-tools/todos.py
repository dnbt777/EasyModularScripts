import os, re, fnmatch

def search_todos_and_assumptions():
    # Configuration
    ignore_dirs = ['.git', 'node_modules', 'venv', '.venv', '__pycache__', 'build', 'dist']
    ignore_file_patterns = ['*.pyc', '*.pyo', '*.so', '*.dll', '*.exe', '*.pdf', '*.jpg', '*.png']
    categories = ['TODO', 'ASSUMPTION', 'OPTIMIZATION']
    
    # Dictionary to store findings by category
    findings = {}
    
    # Walk through all directories and files
    for root, dirs, files in os.walk('.'):
        # Remove ignored directories from dirs to prevent recursion into them
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_dirs)]
        
        for file in files:
            # Skip files matching ignore patterns
            if any(fnmatch.fnmatch(file, pattern) for pattern in ignore_file_patterns):
                continue
                
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    # Check each line for comments
                    for i, line in enumerate(f):
                        # Look for comments with category markers
                        match = re.search(r'#\s*(\w+)\s*:?\s*(.*)', line)
                        if match:
                            category, note = match.groups()
                            if category in categories:
                                # Add to our findings
                                findings.setdefault(category, []).append((path, i+1, note.strip()))
            except (UnicodeDecodeError, IOError):
                # Skip files that can't be read as text
                continue
    
    # Print the report
    for category in findings:
        print(f"{category}S")  # Pluralize the category
        previous_path = ''
        for path, line_num, note in findings[category]:
            if path != previous_path:
                print(f"\t{path}")
                previous_path = path
            print(f"\t\tline {line_num}: {note}")
        #print()  # Empty line between categories

search_todos_and_assumptions()

