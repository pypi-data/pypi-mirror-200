# -*- coding: utf-8 -*-
"""
Created on Feb 27 2023

@author: Philippe@loco-labs.io

The `ntv` module is part of the `NTV.json_ntv` package ([specification document](
https://github.com/loco-philippe/NTV/blob/main/documentation/JSON-NTV-standard.pdf)).

It contains the classes `NtvSingle`, `NtvSet`, `NtvList`, `Ntv`(abstract),
`NtvConnector` and `NtvError` for NTV entities.

# 1 - JSON-NTV structure

The NTV triplet (name, type, value) is represented using a JSON-NTV format inspired
by the RFC [JSON-ND](https://github.com/glenkleidon/JSON-ND) project :
- **```value```** (if name and type are not documented)
- **```{ "name" : value }```** (if name is documented but not type)
- **```{ ":type" : value }```** for primitive entities and **```{ "::type" : value }```**
 for structured entities (if type is documented but not name)
- **```{ "name:type" : value }```** for primitive entities and **```{
 "name::type" : value }```** for structured entities (if type and name are documented).

For an NTV-single, the value is the JSON-value of the entity.
For an NTV-list, value is a JSON-array where JSON-elements are the JSON-NTV formats
 of included NTV entities.
For an NTV-set, value is a JSON-object where JSON-members are the JSON-members of
the JSON-NTV formats of included NTV entities.

This JSON-NTV format allows full compatibility with existing JSON structures:
- a JSON-number, JSON-string or JSON-boolean is the representation of an NTV-single entity,
- a JSON-object with a single member is the representation of an NTV-single entity
- a JSON-array is the representation of an NTV-list entity
- a JSON-object without a single member is the representation of an NTV-set entity

# 2 - Examples of JSON-NTV representations
- NTV-single, simple format :
   - ```"lyon"```
   - ```52.5```
- NTV-single, named format :
   - ```{ "paris:point" : [2.3522, 48.8566] }```
   - ```{ ":point" : [4.8357, 45.7640] }```
   - ```{ "city" : "paris" }```
- NTV-list, simple format :
   - ```[ [2.3522, 48.8566], {"lyon" : [4.8357, 45.7640]} ]```
   - ```[ { ":point" : [2.3522, 48.8566]}, {":point" : [4.8357, 45.7640]} ]```
   - ```[ 4, 45 ]```
   - ```[ "paris" ]```
   - ```[ ]```
- NTV-list, named format :
   - ```{ "cities::point" : [ [2.3522, 48.8566], [4.8357, 45.7640] ] }```
   - ```{ "::point" : [ [2.3522, 48.8566], {"lyon" : [4.8357, 45.7640]} ] }```
   - ```{ "simple list" : [ 4, 45.7 ] }```
   - ```{ "generic date::dat" : [ "2022-01-28T18-23-54Z", "2022-01-28", 1234.78 ] }```
- NTV-set, simple format :
   - ```{ "nom”: "white", "prenom": "walter", "surnom": "heisenberg" }```
   - ```{ "paris:point" : [2.3522, 48.8566] , "lyon" : "france" }```
   - ```{ "paris" : [2.3522, 48.8566], "" : [4.8357, 45.7640] }```
   - ```{ }```
- NTV-set, named format :
   - ```{ "cities::point": { "paris": [2.352, 48.856], "lyon": [4.835, 45.764]}}```
   - ```{ "cities" :     { "paris:point" : [2.3522, 48.8566] , "lyon" : "france"} }```
   - ```{ "city" : { "paris" : [2.3522, 48.8566] } }```

"""
from abc import ABC
import datetime
import json
from json import JSONDecodeError

import cbor2
from shapely import geometry
from json_ntv.namespace import NtvType, Namespace, str_type

class Ntv(ABC):
    ''' The Ntv class is an abstract class used for all NTV entities.

    *Attributes :*

    - **ntv_name** : String - name of the NTV entity
    - **ntv_type**: NtvType - type of the entity
    - **ntv_value**:  value of the entity

    *dynamic values (@property)*
    - `type_str`
    - `code_ntv`

    The methods defined in this class are :

    *Ntv constructor*
    - `obj` *(classmethod)*
    - `from_obj` *(staticmethod)*
    - `from_att` *(staticmethod)*

    *instance methods*
    - `set_name`
    - `set_type`
    - `set_value`
    - `to_obj`
    - `to_repr`
    '''

    # def __init__(self, ntv_value, ntv_name=None, ntv_type=None):
    def __init__(self, ntv_value, ntv_name, ntv_type):
        '''Ntv constructor.

        *Parameters*

        - **ntv_value**: Json entity - value of the entity
        - **ntv_name** : String (default None) - name of the NTV entity
        - **ntv_type**: String or NtvType or Namespace (default None) - type of the entity
        '''
        if isinstance(ntv_type, (NtvType, Namespace)):
            self.ntv_type = ntv_type
        elif ntv_type and ntv_type[-1] != '.':
            self.ntv_type = NtvType.add(ntv_type)
        elif ntv_type and ntv_type[-1] == '.':
            self.ntv_type = Namespace.add(ntv_type)
        else:
            self.ntv_type = None
        if not isinstance(ntv_name, str):
            ntv_name = ''
        self.ntv_name = ntv_name
        self.ntv_value = ntv_value

    @classmethod
    def obj(cls, data):
        ''' return an Ntv entity from data.
        Data can be :
        - a tuple with value, name, typ and cat (see `from_att` method)
        - a value to decode (see `from_obj`method)'''
        if isinstance(data, tuple):
            return cls.from_att(*data)
        return cls.from_obj(data)

    @staticmethod
    def from_att(value, name, typ, cat):
        ''' return an Ntv entity.

        *Parameters*

        - **value**: Ntv entity or value to convert in an Ntv entity
        - **name** : string - name of the Ntv entity
        - **typ** : string or NtvType - type of the NTV entity
        - **cat**: string - NTV category ('single', 'list' or 'set')'''
        value = Ntv._from_value(value)
        if value.__class__.__name__ in ['NtvSingle', 'NtvList', 'NtvSet']:
            return value
        if isinstance(value, list) and cat == 'list':
            return NtvList(value, name, typ)
        if isinstance(value, list) and cat == 'set':
            return NtvSet(value, name, typ)
        if cat == 'single':
            return NtvSingle(value, name, typ)
        return Ntv.from_obj(value, def_type=typ)

    @staticmethod
    def from_obj(value, def_type=None, def_sep=None):
        ''' return an Ntv entity from an object value.

        *Parameters*

        - **value**: value to convert in an Ntv entity
        - **def_type** : NtvType or Namespace (default None) - default type of the NTV entity
        - **def_sep**: ':', '::' or None (default None) - default separator of the Ntv entity'''
        value = Ntv._from_value(value)
        if value.__class__.__name__ in ['NtvSingle', 'NtvList', 'NtvSet']:
            return value
        ntv_name, str_typ, ntv_value, sep = Ntv._decode(value)
        if not sep:
            sep = def_sep
        if isinstance(ntv_value, list) and sep in (None, '::'):
            def_type = NtvType._agreg_type(str_typ, def_type, False)
            if sep and not def_type:
                sep = None
            if sep:
                sep = ':'
            ntv_list = [Ntv.from_obj(val, def_type, sep) for val in ntv_value]
            return NtvList(ntv_list, ntv_name, def_type)
        if sep == ':':
            ntv_type = NtvType._agreg_type(str_typ, def_type, False)
            return NtvSingle(ntv_value, ntv_name, ntv_type,)
        if sep is None and not isinstance(ntv_value, dict):
            is_json = isinstance(value, (int, str, float, bool))
            ntv_type = NtvType._agreg_type(str_typ, def_type, is_json)
            return NtvSingle(ntv_value, ntv_name, ntv_type)
        if isinstance(ntv_value, dict) and (sep == '::' or len(ntv_value) != 1 and
                                            sep is None):
            keys = list(ntv_value.keys())
            values = list(ntv_value.values())
            def_type = NtvType._agreg_type(str_typ, def_type, False)
            if sep and not def_type:
                sep = None
            if sep:
                sep = ':'
            ntv_list = [Ntv.from_obj({key: val}, def_type, sep)
                        for key, val in zip(keys, values)]
            return NtvSet(ntv_list, ntv_name, def_type,)
        if isinstance(ntv_value, dict) and len(ntv_value) == 1 and sep in (None, ':'):
            ntv_type = NtvType._agreg_type(str_typ, def_type, True)
            ntv_single = Ntv.from_obj(ntv_value, ntv_type, sep)
            return NtvSingle(ntv_single, ntv_name, ntv_type)
        raise NtvError('separator ":" is not compatible with value')

    @staticmethod
    def _from_value(value):
        '''return a decoded value'''
        if isinstance(value, str) and value.lstrip() and value.lstrip()[0] in '"-{[0123456789':
            try:
                value = json.loads(value)
            except JSONDecodeError:
                pass
        string = isinstance(value, str)
        if value is None or (string and value == 'null'):
            return NtvSingle(None)
        if string and value == 'true':
            return NtvSingle(True)
        if string and value == 'false':
            return NtvSingle(False)
        return value

    def __len__(self):
        ''' len of ntv_value'''
        if isinstance(self.ntv_value, (list, set)):
            return len(self.ntv_value)
        return 1

    def __str__(self):
        '''return string format'''
        return self.to_obj(encoded=True)

    def __repr__(self):
        '''return classname and code'''
        return json.dumps(self.to_repr(False, False, False, 10))

    def __contains__(self, item):
        ''' item of Ntv entities'''
        return item in self.ntv_value

    def __getitem__(self, ind):
        ''' return ntv_value item (value conversion)'''
        if isinstance(ind, tuple):
            return [self.ntv_value[i] for i in ind]
        return self.ntv_value[ind]

    def __setitem__(self, ind, value):
        ''' modify ntv_value item'''
        if ind < 0 or ind >= len(self):
            raise NtvError("out of bounds")
        self.ntv_value[ind] = value

    def __delitem__(self, ind):
        '''remove a ntv_value item'''
        self.ntv_value.pop(ind)

    @property
    def type_str(self):
        '''return a string with the value of the NtvType of the entity'''
        if not self.ntv_type:
            return None
        return self.ntv_type.long_name

    @property
    def code_ntv(self):
        '''return a string with the NTV code composed with :
        - 'l' (for NtvList), 's' (for NtvSet) or 'v' (for NtvSingle)
        - 'N' if ntv_name is present
        - 'T' if ntv_type is present'''
        dic = {'NtvList': 'l', 'NtvSet': 's', 'NtvSingle': 'v'}
        code = dic[self.__class__.__name__]
        if self.ntv_name:
            code += 'N'
        if self.ntv_type and self.ntv_type.long_name != 'json':
            code += 'T'
        return code

    def set_name(self, name):
        '''set a new name to the entity'''
        if name and not isinstance(name, str):
            raise NtvError('the name is not a string')
        if not name:
            name = ''
        self.ntv_name = name

    def set_type(self, typ=None):
        '''set a new type to the entity (available only for NtvSingle)'''
        if typ and not isinstance(typ, (str, NtvType, Namespace)):
            raise NtvError('the type is not a valid type')
        if self.__class__.__name__ != 'NtvSingle':
            raise NtvError('set_type is available only for NtvSingle class')
        self.ntv_type = str_type(typ, True)

    def to_repr(self, nam=True, typ=True, val=True, maxi=10):
        '''return a simple json representation of the Ntv entity.

        *Parameters*

        - **nam**: Boolean (default True) : if true, the names are included
        - **typ**: Boolean (default True) : if true, the types are included
        - **val**: Boolean (default True) : if true, the values are included
        - **maxi**: Integer (default 10) : number of values to included for NtvList
        or NtvSet entities. If maxi < 1 all the values are included.
        '''
        ntv = self.code_ntv
        if nam and typ:
            ntv = ntv[0]
        if self.ntv_name and nam:
            ntv += '-' + self.ntv_name
        if self.ntv_type and typ:
            ntv += '-' + self.ntv_type.long_name
        if isinstance(self, NtvSingle) and not isinstance(self.ntv_value, NtvSingle):
            if val:
                if ntv:
                    ntv += '-'
                ntv += json.dumps(self.ntv_value)
            return ntv
        if isinstance(self, NtvSingle) and isinstance(self.ntv_value, NtvSingle):
            return {ntv:  self.ntv_value.to_repr(nam, typ, val)}
        if isinstance(self, (NtvList, NtvSet)):
            if maxi < 1:
                maxi = len(self.ntv_value)
            return {ntv:  [ntvi.to_repr(nam, typ, val) for ntvi in self.ntv_value[:maxi]]}
        raise NtvError('the ntv entity is not consistent')

    def to_obj(self, def_type=None, **kwargs):
        '''return the JSON representation of the NTV entity (json-ntv format).

        *Parameters*

        - **def_type** : NtvType or Namespace (default None) - default type to apply
        to the NTV entity
        - **encoded** : boolean (default False) - choice for return format
        (string/bytes if True, dict/list/tuple else)
        - **encode_format**  : string (default 'json')- choice for return format
        (json, cbor, tuple, obj)
        - **simpleval** : boolean (default False) - if True, only value (without
        name and type) is included
        '''
        option = {'encoded': False, 'encode_format': 'json',
                  'simpleval': False} | kwargs
        value = self._obj_value(**option)
        obj_name = self._obj_name(def_type)
        if option['simpleval']:
            name = ''
        elif option['encode_format'] in ('cbor', 'obj') and not Ntv._is_json_ntv(value):
            name = obj_name[0]
        else:
            name = obj_name[0] + obj_name[1] + obj_name[2]
        if not name:
            json_obj = value
        else:
            json_obj = {name: value}
        if option['encoded'] and option['encode_format'] == 'json':
            return json.dumps(json_obj)
        if option['encoded'] and option['encode_format'] == 'cbor':
            return cbor2.dumps(json_obj, datetime_as_timestamp=True,
                               timezone=datetime.timezone.utc, canonical=True,
                               date_as_datetime=True)
        return json_obj

    def to_tuple(self, maxi=10):
        '''return the JSON representation of the NTV entity (json-ntv format).

        *Parameters*

        - **def_type** : NtvType or Namespace (default None) - default type to apply
        to the NTV entity
        - **encoded** : boolean (default False) - choice for return format
        (string/bytes if True, dict/list/tuple else)
        - **encode_format**  : string (default 'json')- choice for return format
        (json, cbor, tuple, obj)
        - **simpleval** : boolean (default False) - if True, only value (without
        name and type) is included
        '''
        clas = self.__class__.__name__
        val = self.ntv_value
        name = self.ntv_name
        typ = None
        if self.ntv_type:
            typ = self.ntv_type.long_name
        if isinstance(self, NtvSingle) and not isinstance(val, NtvSingle):
            return (clas, name, typ, val)
        if isinstance(self, NtvSingle) and isinstance(val, NtvSingle):
            return (clas, name, typ, val.to_tuple(maxi=maxi))
        if isinstance(self, (NtvList, NtvSet)):
            if maxi < 1:
                maxi = len(val)
            return (clas, name, typ, [ntv.to_tuple(maxi=maxi) for ntv in val[:maxi]])
        raise NtvError('the ntv entity is not consistent')

    def _obj_value(self):
        return ''

    def _obj_name(self, def_type=None):
        '''return the JSON name of the NTV entity (json-ntv format)

        *Parameters*

        - **def_typ** : NtvType or Namespace (default None) - type of the parent entity'''
        if def_type is None:
            def_type = ''
        elif isinstance(def_type, (NtvSingle, Namespace)):
            def_type = def_type.long_name
        json_name = ''
        if self.ntv_name:
            json_name = self.ntv_name
        ntv_type = ''
        if self.ntv_type:
            ntv_type = self.ntv_type.long_name
        if not ntv_type:
            json_type = def_type
        else:
            json_type = NtvType._relative_type(def_type, ntv_type)
        json_sep = ''
        if json_type or (len(self.ntv_value) == 1 and self.__class__.__name__ == 'NtvSet'):
            json_sep = '::'
        return (json_name, json_sep, json_type)

    @staticmethod
    def _decode(json_value):
        '''return (name, type, value, separator) of the json value'''
        if json_value is None:
            return (None, None, None, None)
        if isinstance(json_value, (list, int, str, float, bool)):
            return (None, None, json_value, None)
        if isinstance(json_value, dict) and len(json_value) != 1:
            return (None, None, json_value, None)
        if isinstance(json_value, dict) and len(json_value) == 1:
            json_name = list(json_value.keys())[0]
            val = json_value[json_name]
            nam, typ, sep = Ntv._from_obj_name(json_name)
            return (nam, typ, val, sep)
        return(*Ntv._cast(json_value), ':')

    @staticmethod
    def _cast(data):
        '''return (name, type, value) of the data'''
        dic_geo_cl = {'point': 'point', 'multipoint': 'multipoint', 'linestring': 'line',
                      'multilinestring': 'multiline', 'polygon': 'polygon',
                      'multipolygon': 'multipolygon'}
        #dic_connec = {'series': 'SeriesConnec', 'dataframe': 'DataFrameConnec'}
        dic_connec = NtvConnector.dic_connec()
        clas = data.__class__.__name__.lower()
        match clas:
            case 'date':
                return (None, 'date', data.isoformat())
            case 'time':
                return (None, 'time', data.isoformat())
            case 'datetime':
                return (None, 'datetime', data.isoformat())
            case 'point' | 'multipoint' | 'linestring' | 'multilinestring' | \
                    'polygon' | 'multipolygon':
                return (None, dic_geo_cl[data.__class__.__name__.lower()],
                        Ntv._listed(data.__geo_interface__['coordinates']))
            case _:
                connector = None
                if clas in dic_connec and dic_connec[clas] in NtvConnector.connector():
                    connector = NtvConnector.connector()[dic_connec[clas]]
                if connector:
                    return connector.to_ntv(data)
                raise NtvError('connector is not defined to NTV entity')
        return (None, None, None)

    def _uncast(self, **option):
        '''return object from ntv_value'''
        dic_geo = {'point': 'point', 'multipoint': 'multipoint', 'line': 'linestring',
                   'multiline': 'multilinestring', 'polygon': 'polygon',
                   'multipolygon': 'multipolygon'}
        dic_cbor = {'point': False, 'multipoint': False, 'line': False,
                    'multiline': False, 'polygon': False, 'multipolygon': False,
                    'date': True, 'time': False, 'datetime': True}
        dic_obj = {'tab': 'Ilist', 'other': None}
        if 'dicobj' in option:
            dic_obj |= option['dicobj']
        obj = True
        if option['encode_format'] == 'cbor':
            obj = False
            if self.ntv_type and self.ntv_type.name in dic_cbor:
                obj = dic_cbor[self.ntv_type.name]
        if self.ntv_type is None or not obj:
            return self.ntv_value
        match self.ntv_type.name:
            case 'date':
                return datetime.date.fromisoformat(self.ntv_value)
            case 'time':
                return datetime.time.fromisoformat(self.ntv_value)
            case 'datetime':
                return datetime.datetime.fromisoformat(self.ntv_value)
            case 'point' | 'multipoint' | 'line' | \
                 'multiline' | 'polygon' | 'multipolygon':
                return geometry.shape({"type": dic_geo[self.ntv_type.name],
                                      "coordinates": self.ntv_value})
            case _:
                connector = None
                if self.ntv_type.name in dic_obj and \
                        dic_obj[self.ntv_type.name] in NtvConnector.connector():
                    connector = NtvConnector.connector(
                    )[dic_obj[self.ntv_type.name]]
                elif dic_obj['other'] in NtvConnector.connector():
                    connector = NtvConnector.connector()['other']
                if connector:
                    return connector.from_ntv(self.ntv_value)
                return self.ntv_value

    @staticmethod
    def _from_obj_name(string):
        '''return a tuple with name, type ans separator from string'''
        if not isinstance(string, str):
            raise NtvError('a json-name have to be str')
        if string == '':
            return (None, None, None)
        sep = None
        if '::' in string:
            sep = '::'
        elif ':' in string:
            sep = ':'
        if sep is None:
            return (string, None, None)
        split = string.rsplit(sep, 2)
        if len(split) == 1:
            return (string, None, sep)
        if split[0] == '':
            return (None, split[1], sep)
        if split[1] == '':
            return (split[0], None, sep)
        return (split[0], split[1], sep)

    @staticmethod
    def _is_json_ntv(val):
        ''' return True if val is a json type'''
        return val is None or isinstance(val, (list, int, str, float, bool, dict))

    @staticmethod
    def _listed(idx):
        '''transform a tuple of tuple in a list of list'''
        return [val if not isinstance(val, tuple) else Ntv._listed(val) for val in idx]

class NtvSingle(Ntv):
    ''' An NTV-single entity is a Ntv entity not composed with other entities.

    *Attributes :*

    - **ntv_name** : String - name of the NTV entity
    - **ntv_type**: NtvType - type of the entity
    - **ntv_value**:  value of the entity

    *dynamic values (@property)*
    - `type_str`
    - `code_ntv`

    The methods defined in this class are :

    *Ntv constructor*
    - `obj`
    - `from_obj`
    - `from_att`

    *instance methods*
    - `set_name`
    - `set_type`
    - `set_value`
    - `to_obj`
    - `to_repr`
    '''

    def __init__(self, value, ntv_name=None, ntv_type=None):
        '''NtvSingle constructor.

        *Parameters*

        - **ntv_name** : String (default None) - name of the NTV entity
        - **ntv_type**: String (default None) - type of the entity
        - **value**: value of the entity
        '''
        is_json_ntv = Ntv._is_json_ntv(value) or isinstance(value, NtvSingle)
        if not ntv_type and is_json_ntv:
            ntv_type = 'json'
        if not ntv_type and not is_json_ntv:
            name, ntv_type, value = Ntv._cast(value)
            if not ntv_name:
                ntv_name = name
        elif ntv_type and not is_json_ntv:
            raise NtvError('ntv_value is not compatible with ntv_type')
        if ntv_type and isinstance(ntv_type, str) and ntv_type[-1] == '.':
            raise NtvError('the ntv_type is not valid')
        super().__init__(value, ntv_name, ntv_type)

    def __eq__(self, other):
        ''' equal if name type and value are equal'''
        return self.__class__.__name__ == other.__class__.__name__ and\
            self.ntv_name == other.ntv_name and self.ntv_type == other.ntv_type and\
            self.ntv_value == other.ntv_value

    def _obj_value(self, **kwargs):
        '''return the Json format of the ntv_value'''
        option = {'encoded': False, 'encode_format': 'json',
                  'simpleval': False} | kwargs
        if isinstance(self.ntv_value, NtvSingle):
            def_type = ''
            if self.ntv_type:
                def_type = self.ntv_type.long_name
            option2 = option | {'encoded': False}
            return self.ntv_value.to_obj(def_type=def_type, **option2)
        if option['encode_format'] in ('json', 'tuple'):
            return self.ntv_value
        return Ntv._uncast(self, **option)

    def _obj_name(self, def_type=None):
        '''return the JSON name of the NTV entity (json-ntv format)

        *Parameters*

        - **def_typ** : NtvType or Namespace (default None) - type of the parent entity'''
        if def_type is None:
            def_type = ''
        elif isinstance(def_type, (NtvSingle, Namespace)):
            def_type = def_type.long_name
        json_name = ''
        if self.ntv_name:
            json_name = self.ntv_name
        json_type = NtvType._relative_type(def_type, self.ntv_type.long_name)
        json_sep = ''
        if json_type:
            json_sep = ':'
        if json_type == 'json' and (not def_type or def_type == 'json'):
            json_type = ''
            if not isinstance(self.ntv_value, list) and \
               not (isinstance(self.ntv_value, dict) and len(self.ntv_value) != 1):
                json_sep = ''
        return (json_name, json_sep, json_type)


class NtvList(Ntv):
    '''An NTV-list entity is a Ntv entity where:

    - ntv_value is a list of NTV entities,
    - ntv_type is a default type available for included NTV entities

    *Attributes :*

    - **ntv_name** : String - name of the NTV entity
    - **ntv_type**: NtvType - type of the entity
    - **ntv_value**:  value of the entity

    The methods defined in this class are :

    *Ntv constructor*
    - `obj`
    - `from_obj`
    - `from_att`

    *dynamic values (@property)*
    - `type_str`
    - `code_ntv`

    *instance methods*
    - `set_name`
    - `set_type`
    - `set_value`
    - `to_obj`
    - `to_repr`
    '''

    def __init__(self, list_ntv, ntv_name=None, ntv_type=None):
        '''NtvList constructor.

        *Parameters*

        - **ntv_name** : String (default None) - name of the NTV entity
        - **ntv_type**: String (default None) - default type or namespace of the included entities
        - **list_ntv**: list - list of Ntv objects or obj_value of Ntv objectd
        '''
        if isinstance(list_ntv, (NtvList, NtvSet)):
            ntv_value = list_ntv.ntv_value
            ntv_type = list_ntv.ntv_type
            ntv_name = list_ntv.ntv_name
        elif isinstance(list_ntv, list):
            ntv_value = [Ntv.from_obj(ntv, ntv_type, ':') for ntv in list_ntv]
        else:
            raise NtvError('ntv_value is not a list')
        if not ntv_type and len(ntv_value) > 0 and ntv_value[0].ntv_type and \
                ntv_value[0].ntv_type.long_name != 'json':
            ntv_type = ntv_value[0].ntv_type
        super().__init__(ntv_value, ntv_name, ntv_type)

    def __eq__(self, other):
        ''' equal if name and value are equal'''
        return self.__class__.__name__ == other.__class__.__name__ and\
            self.ntv_name == other.ntv_name and self.ntv_value == other.ntv_value

    def _obj_value(self, **kwargs):
        '''return the Json format of the ntv_value'''
        option = {'encoded': False, 'encode_format': 'json',
                  'simpleval': False} | kwargs
        option2 = option | {'encoded': False}
        def_type = ''
        if self.ntv_type:
            def_type = self.ntv_type.long_name
        return [ntv.to_obj(def_type=def_type, **option2) for ntv in self.ntv_value]


class NtvSet(Ntv):
    '''An NTV-set entity is a Ntv entity where:

    - ntv_value is a list of NTV entities,
    - ntv_type is a default type available for included NTV entities

    *Attributes :*

    - **ntv_name** : String - name of the NTV entity
    - **ntv_type**: NtvType - type of the entity
    - **ntv_value**:  value of the entity

    The methods defined in this class are :

    *Ntv constructor*
    - `obj`
    - `from_obj`
    - `from_att`

    *dynamic values (@property)*
    - `type_str`
    - `code_ntv`

    *instance methods*
    - `set_name`
    - `set_type`
    - `set_value`
    - `to_obj`
    - `to_repr`
    '''

    def __init__(self, list_ntv, ntv_name=None, ntv_type=None):
        '''NtvSet constructor.

        *Parameters*

        - **ntv_name** : String (default None) - name of the NTV entity
        - **ntv_type**: String (default None) - default type or namespace of the included entities
        - **list_ntv**: list - list of Ntv objects or obj_value
        '''
        if isinstance(list_ntv, (NtvList, NtvSet)):
            ntv_value = list_ntv.ntv_value
            ntv_type = list_ntv.ntv_type
            ntv_name = list_ntv.ntv_name
        elif isinstance(list_ntv, list):
            ntv_value = [Ntv.from_obj(ntv, ntv_type, ':') for ntv in list_ntv]
        else:
            raise NtvError('ntv_value is not a list')
        super().__init__(ntv_value, ntv_name, ntv_type)

    def __eq__(self, other):
        ''' equal if name and value are equal'''
        return self.__class__.__name__ == other.__class__.__name__ and\
            self.ntv_name == other.ntv_name and self.ntv_value == other.ntv_value

    def _obj_value(self, **kwargs):
        '''return the Json format of the ntv_value'''
        option = {'encoded': False, 'encode_format': 'json',
                  'simpleval': False} | kwargs
        option2 = option | {'encoded': False}
        def_type = ''
        if self.ntv_type:
            def_type = self.ntv_type.long_name
        return {list(ntv.to_obj(def_type=def_type, **option2).items())[0][0]:
                list(ntv.to_obj(def_type=def_type, **option2).items())[0][1]
                for ntv in self.ntv_value}


class NtvConnector(ABC):
    ''' The NtvConnector class is an abstract class used for all NTV connectors.
    A NTV connector has two methods for conversion between NTV data and an object'''

    @classmethod
    def connector(cls):
        '''return a dict with the connectors: { name: class }'''
        return {clas.__name__: clas for clas in cls.__subclasses__()}

    @classmethod
    def dic_connec(cls):
        '''return a dict with the clas associated to the connector:
        { clas_obj: classconnector }'''
        return {clas.clas_obj: clas.__name__ for clas in cls.__subclasses__()}


class NtvError(Exception):
    ''' NTV Exception'''
    # pass
