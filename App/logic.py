"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones
 *
 * Dario Correal
 """

import os
import csv
import datetime
import DataStructures.Tree.binary_search_tree as bst
import DataStructures.List.array_list as al
import DataStructures.Map.map_linear_probing as lp
# TODO Realice la importación del Árbol Binario Ordenado
# TODO Realice la importación de ArrayList (al) como estructura de datos auxiliar para sus requerimientos
# TODO Realice la importación de LinearProbing (lp) como estructura de datos auxiliar para sus requerimientos


data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'



def new_logic():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'crimes': None,
                'dateIndex': None
                }

    analyzer['crimes'] = al.new_list()
    
    # Crear el mapa ordenado con el BST
    analyzer['dateIndex'] = bst.new_map()
    
    return analyzer

    

# Funciones para realizar la carga

def load_data(analyzer, crimesfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    crimesfile = data_dir + crimesfile
    input_file = csv.DictReader(open(crimesfile, encoding="utf-8"),
                                delimiter=",")
    for crime in input_file:
        add_crime(analyzer, crime)
    return analyzer



# Funciones para agregar informacion al analizador


def add_crime(analyzer, crime):
    """
    funcion que agrega un crimen al catalogo
    """
    al.add_last(analyzer['crimes'], crime)
    update_date_index(analyzer['dateIndex'], crime)
    return analyzer


def update_date_index(map, crime):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = crime['OCCURRED_ON_DATE']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    the_date = crimedate.date()
    entry = bst.get(map, crimedate.date())
    if entry is None:
        datentry = new_data_entry(crime)
        # Insertar la nueva entrada en el BST
        map = bst.put(map, the_date, datentry)
        
    else:
        datentry = entry
    add_date_index(datentry, crime)
    return map


# Se asume que 'al' y 'lp' son módulos o alias con las funciones new_list, add_last, get, y put

def add_date_index(datentry, crime):
    """
    Actualiza un indice de tipo de crimenes. Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstcrimes']
    al.add_last(lst, crime)
    
    offenseIndex = datentry['offenseIndex']
    offense_type = crime['OFFENSE_CODE_GROUP']
    
    # Intenta obtener la lista de crímenes para este tipo de ofensa (si ya existe)
    offentry_list = lp.get(offenseIndex, offense_type)
    
    if (offentry_list is None):
        # CASO 1: No se encuentra el tipo de crimen (Es la primera vez que ocurre en esta fecha)
        
        # 1. Crear una nueva lista de crímenes para este tipo de ofensa
        new_list_for_offense = al.new_list() # asumiendo que al.new_list crea una lista vacía
        
        # 2. Agregar el crimen actual a la nueva lista
        al.add_last(new_list_for_offense, crime)
        
        # 3. Insertar esta nueva lista en la tabla hash (offenseIndex)
        lp.put(offenseIndex, offense_type, new_list_for_offense)
        
    else:
        # CASO 2: Ya se encuentra el tipo de crimen (Ya existe una lista para este tipo)
        
        # 1. Simplemente agregar el crimen actual al final de la lista existente
        al.add_last(offentry_list, crime)
        
    return datentry


def new_data_entry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstcrimes': None}
    entry['offenseIndex'] = lp.new_map(num_elements=30,
                                        load_factor=0.5)
    entry['lstcrimes'] = al.new_list()
    return entry


def new_offense_entry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = al.new_list()
    return ofentry


# ==============================
# Funciones de consulta
# ==============================


def crimes_size(analyzer):
    """
    Número de crimenes
    """
    return al.size(analyzer['crimes'])


def index_height(analyzer):
    """
    Altura del arbol
    """
    return bst.height(analyzer['dateIndex'])


def index_size(analyzer):
    """
    Numero de elementos en el indice
    """
    return bst.size(analyzer['dateIndex'])


def min_key(analyzer):
    """
    Llave mas pequena
    """
    return bst.get_min(analyzer['dateIndex'])


def max_key(analyzer):
    """
    Llave mas grande
    """
    return bst.get_max(analyzer['dateIndex'])


def get_crimes_by_range(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    init_date = datetime.datetime.strptime(initialDate, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(finalDate, '%Y-%m-%d').date()

    total = 0
    lst = analyzer['crimes']
    size = al.size(lst)
    for i in range(size):
        crime = al.get_element(lst, i)
        crimedt = datetime.datetime.strptime(crime['OCCURRED_ON_DATE'], '%Y-%m-%d %H:%M:%S').date()
        if init_date <= crimedt <= end_date:
            total += 1
    return total


def get_crimes_by_range_code(analyzer, initialDate, offensecode):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    the_date = datetime.datetime.strptime(initialDate, '%Y-%m-%d').date()
    datentry = bst.get(analyzer['dateIndex'], the_date)
    if datentry is None:
        return 0

    lst = datentry['lstcrimes']
    total = 0
    size = al.size(lst)
    for i in range(size):
        crime = al.get_element(lst, i)
        if crime['OFFENSE_CODE_GROUP'] == offensecode:
            total += 1
    return total

