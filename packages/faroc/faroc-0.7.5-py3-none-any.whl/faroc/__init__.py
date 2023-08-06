from .faroc import FaRoC_Reader, FaRoC_Writer, FaRoC_Mover

def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def main():
    """Entry point for the application script"""
    print("Welcome to:\n")

    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
        
    FaRoC_ascii_art = read_file(f'{dir_path}/FaRoC_ascii_art')
    

    print(FaRoC_ascii_art)


    print("Fanuc Robot Control")

    print()
    print("The source code is available under:")
    print("https://codeberg.org/hojak/faroc")