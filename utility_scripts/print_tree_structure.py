import os

def display_directory_tree(start_directory, indent=''):
    # List all files and directories in the current directory
    items = os.listdir(start_directory)
    
    # If you have specific directories to exclude, list them here.
    excluded_directories = ['tenacity', 'tomli', 'urllib3', '__pycache__', '.venv','.vscode','.gitignore', '.pio', 'include','lib', '.git','data_logs']  

    for item in items:
        item_path = os.path.join(start_directory, item)
        
        # Check if the current item is a directory
        if os.path.isdir(item_path) and item not in excluded_directories:
            print(indent + item + '/')
            display_directory_tree(item_path, indent=indent + '    ')
        elif not os.path.isdir(item_path):
            print(indent + item)

if __name__ == '__main__':
    directory_to_start = '.'  # Current directory
    display_directory_tree(directory_to_start)
