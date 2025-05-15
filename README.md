# AutoRenamer Script

Renombrador de archivos elegante y seguro. Ideal para ordenar, limpiar y estandarizar archivos con prefijos personalizados, filtros por extensión y vista previa visual.

---

## 🚀 Características principales

- Renombramiento masivo con numeración automática.
- Prefijo personalizado seguro y validado.
- Filtro opcional por extensión `--ext .jpg`.
- Vista previa elegante en table `Rich`.
- Modo simulación `--dry-run`.

## Uso básico

```bash
python app.py -p <ruta> --prefix <prefjo>
```

### Ejemplo:

```bash
python app.py -p ./imagenes --prefix python
```

Esto renombrará:

```bash
DSC_0323.JPG -> python_001.jpg
foto_randomuser.PNG -> python_002.png
```

---

## 🎯 Contribución

Este es un script amigable, puedes personalizarlo fácilmente según tus intenciones. Se aceptan forks, pull requests o sugerencias. Este script lo hice con la intención de organizar mis archivos. 