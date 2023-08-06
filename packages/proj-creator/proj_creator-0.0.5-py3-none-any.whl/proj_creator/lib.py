import os



def write_file(root_dir, path, s):
    full_path = os.path.join(root_dir, path)
    if os.path.exists(full_path):
        with open(full_path, 'w') as f:
            f.write(s)