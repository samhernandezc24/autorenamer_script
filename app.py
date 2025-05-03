from os import makedirs
from os.path import join


def save_file(filepath, data):
    with open(filepath, 'w') as file:
        file.write(data)
        

def generate_line():
    ...
    

def generate_all_files(path='tmp'):
    makedirs(path, exist_ok=True)
    
    for i in range(1000):
        filename = f'file_{i}.txt'
        filepath = join(path, filename)
        
        # Genera el contenido del archivo
        data = generate_line()
        
        # Guarda el archivo en la ruta especificada
        save_file(filepath, data)
    

def main():
    ...
    

if __name__ == '__main__':
    main()
