""" Adapted from:
https://realpython.com/inheritance-composition-python/#mixing-features-with-mixin-classes
"""
import uuid
from stn.utils.uuid import from_str


class AsDictMixin:

    def to_dict(self):
        return {
            prop: self._represent(value)
            for prop, value in self.__dict__.items()
            if not self.is_internal(prop)
        }

    @classmethod
    def _represent(cls, value):
        if isinstance(value, object):
            if hasattr(value, 'to_dict'):
                return value.to_dict()
            elif isinstance(value, uuid.UUID):
                return str(value)
            else:
                return value
        else:
            return value

    @staticmethod
    def is_internal(prop):
        return prop.startswith('_')

    @classmethod
    def from_dict(cls, dict_repr):
        attrs = cls.to_attrs(dict_repr)
        return cls(**attrs)

    @classmethod
    def to_attrs(cls, dict_repr):
        attrs = dict()
        for key, value in dict_repr.items():
            attrs[key] = cls._get_value(key, value)
        return attrs

    @classmethod
    def _get_value(cls, key, value):
        if key in ['task_id', 'pickup_action_id', 'delivery_action_id']:
            return from_str(value)
        else:
            return value
