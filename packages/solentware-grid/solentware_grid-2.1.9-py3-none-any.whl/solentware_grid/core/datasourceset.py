# datasourceset.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide the DataSourceSet class to access a sequence of recordsets.

Nothing significant is implemented.

Would follow dpt.dptdatasourceset.DataSourceSet class if implemented.

"""

from .dataclient import DataSource


class DataSourceSetNotImplemented(Exception):
    """Raise when an attempt to call a method not yet implemented is done."""


class DataSourceSet(DataSource):
    """Provide bsddb3 style cursor access to a sequence of recordsets."""

    def __init__(self, **kwargs):
        """Delegate then initialise key_sets and recordsets attributes."""
        super().__init__(**kwargs)

        self.key_sets = []
        self.recordsets = dict()

    def close(self):
        """Close resources."""
        self._clear_recordsets()

    def get_cursor(self):
        """Return cursor on record set, or list, associated with datasource.

        Not implemented.
        """
        raise DataSourceSetNotImplemented("'get_cursor()' not implemented")

    def get_recordset(self, dbname, key=None, from_=None):
        """Create a recordset of records with key==key.

        Not implemented.
        """
        raise DataSourceSetNotImplemented("'get_recordset()' not implemented")

    def set_recordsets(
        self,
        dbname,
        partial_keys=None,
        constant_keys=None,
        include_without_constant_keys=False,
        population=None,
    ):
        """Create all combinations of partial keys.

        Not implemented.
        """
        raise DataSourceSetNotImplemented("'set_recordsets()' not implemented")

    def _clear_recordsets(self):
        """Destroy all recordsets."""
        self.recordsets.clear()
