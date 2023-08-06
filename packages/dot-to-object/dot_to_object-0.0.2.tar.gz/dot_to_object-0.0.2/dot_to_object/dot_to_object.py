#!/usr/bin/env python
"""
This module is for converting dot notation strings like 'class.object.object'
to actual Python objects. To use this module just initialize the class with
your variables, usally locals(), then use the get method to obtain the object.
"""


class DottoObject:
    def __init__(self, variables):
        self.vars = variables

    def get(self, notation):
        if not isinstance(notation, str):
            raise TypeError('Notation must be a string.')

        obj_gen = (obj for obj in notation.split('.'))
        top_object = next(obj_gen)
        try:
            top_object = self.vars.get(top_object, None)
        except AttributeError:  # if top object doesn't exist
            top_object = None

        for prop in obj_gen:
            try:
                top_object = getattr(top_object, prop)
            except AttributeError:  # if property doesn't exist
                top_object = None
        
        return top_object
