# Decoupe2D

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Découper dans plusieurs plans 2D des rectangles plus petis avec rotation
# Installation

Python 3.7  au minimum

```bash
$ mkdir Decoupe2D
$ cd Decoupe2D
$ python3.7 -m pip install matplotlib
$ git clone https://github.com/idealsonDEV/Decoupe2D.git
```

# Utilisation

Format d'entrée:
```python
morceaux = [ 
                (2, 2, '2x2'), # width, height,label
                (1, 3, '1x3'), 
                (4, 3, '4x3'), 
                (3, 1, '3x1'), 
                (3, 4, '3x4'), 
                (2, 2, '2x2')
            ]
plans = [
                (6, 6), width, height
                (6, 6)
            ]
```
Format de sortie
```python
(2, [   # Nombre de plan utilisé
      (0, 0, 0, 4, 3, '4x3'),  # Index du plan , x , y, width, height, label
      (0, 0, 3, 4, 3, '3x4'), 
      (0, 4, 0, 2, 2, '2x2'), 
      (0, 4, 2, 2, 2, '2x2'), 
      (1, 0, 0, 1, 3, '1x3'), 
      (1, 0, 3, 1, 3, '3x1')
    ])
 ```
 Résolution
 ```python
nplans, mor_list = Solver2D(morceaux,plans)
 ```
 Afficher le resultat
 ```python
Show2D(nplans, mor_list)
 ```
 Imprimer le résulat
  ```python
PrintPDF2D(nplans, mor_list)
 ```
