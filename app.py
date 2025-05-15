import argparse
import humanize
import logging
import re

from pathlib import Path
from rich.console import Console
from rich.table import Table

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

console = Console()


# --- Funciones principales --- #

def get_files(path: Path, ext_filter: str = None):
    files = [f for f in path.iterdir() if f.is_file()]
    if ext_filter:
        files = [f for f in files if f.suffix.lower() == ext_filter.lower()]
    return sorted(files)


def show_preview(files, path, prefix):
    table = Table(title='Vista previa de renombramiento', show_header=True, header_style='bold magenta')
    table.add_column('Original', style='cyan')
    table.add_column('Nuevo nombre', style='green')
    table.add_column('Tamaño', style='yellow')
    
    for index, file in enumerate(files, start=1):
        new_filename = f'{prefix}_{index:03}{file.suffix.lower()}'
        size = humanize.naturalsize(file.stat().st_size)
        table.add_row(file.name, new_filename, size)
    
    console.print(table)
    return table


def check_conflicts(files, path, prefix):
    conflicts = []
    for index, file in enumerate(files, start=1):
        new_filename = f'{prefix}_{index:03}{file.suffix.lower()}'
        new_filepath = path / new_filename
        if new_filepath.exists() and new_filepath != file:
            conflicts.append(new_filename)
    return conflicts


def rename_files(path: Path, dry_run: bool, prefix: str, ext_filter: str) -> None:
    if not path.exists() or not path.is_dir():
        logging.error(f'Ruta inválida: {path}')
        return
    
    files = get_files(path, ext_filter)
    
    if not files:
        logging.warning(f'No se encontraron archivos en {path}')
        return
    
    # Mostrar preview primero
    show_preview(files, path, prefix)
    
    # Validar conflictos antes de ejecutar
    conflicts = check_conflicts(files, path, prefix)
    if conflicts:
        logging.error(f'Se detectaron conflictos de nombres en el destino:\n{conflicts}')
        logging.error('Renombramiento abortado.')
        return
    
    if dry_run:
        logging.info('Modo simulación activado (--dry-run). No se renombrará ningún archivo.')
        return    
    
    confirm = console.input("[bold yellow]¿Deseas continuar con el renombramiento? (y/n): [/]")
    if confirm.lower() != 'y':
        logging.info('Operación cancelada por el usuario.')
        return
    
    # Proceder con renombrado seguro
    for index, file in enumerate(files, start=1):
        new_filename = f'{prefix}_{index:03}{file.suffix.lower()}'
        new_filepath = path / new_filename            
        logging.info(f'Renombrando: {file.name} -> {new_filename}')
        file.rename(new_filepath)
        

def is_valid_prefix(prefix):
    return re.match(r'^[\w\-]+$', prefix) is not None
        
        
# --- Argumentos CLI --- #        
        
def parse_args():
    parser = argparse.ArgumentParser(
        description='Renombrador de archivos con formato limpio, ordenado y prefijo personalizado.'
    )    
    parser.add_argument(
        '-p', '--path',
        type=Path,
        required=True,
        help='Ruta donde están los archivos a renombrar'        
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simula el renombramiento sin hacer cambios reales'
    )
    parser.add_argument(
        '--prefix',
        type=str,
        default='file',
        help='Prefijo personalizado para los nuevos archivos (por defecto: file)'
    )
    parser.add_argument(
        '--ext',
        type=str,
        help='Filtrar archivos por extensión específica, por ejemplo: .jpg, .png'
    )
    return parser.parse_args()
    

def main():
    args = parse_args()
    
    if not is_valid_prefix(args.prefix):
        logging.error('Prefijo inválido. Solo se permiten letras, números, guiones bajos y guiones medios.')
        return
    
    rename_files(args.path, args.dry_run, args.prefix, args.ext)
    

if __name__ == '__main__':
    main()
