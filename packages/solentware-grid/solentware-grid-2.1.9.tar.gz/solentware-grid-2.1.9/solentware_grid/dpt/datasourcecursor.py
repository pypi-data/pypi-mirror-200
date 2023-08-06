# datasourcecursor.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide DataSourceClass class to access a DPT database.

The dptdb package is used to access the DPT database.
"""

from dptdb import dptapi

from ..core.dataclient import DataSource


class DataSourceCursor(DataSource):
    """Provide bsddb3 style cursor access to recordset of arbitrary records."""

    def __init__(self, *a, **k):
        """Delegate then initialise recordset and _fieldvalue attributes."""
        super().__init__(*a, **k)

        self.recordset = None
        self._fieldvalue = dptapi.APIFieldValue()
        # self.dbhome.table[self.dbset]._sources[self] = None

    def close(self):
        """Destroy the APIRecordSet created by DPT to implement recordset."""
        if self.recordset is not None:
            try:
                del self.dbhome.table[self.dbset]._sources[self]
            except:
                pass
            # self.dbhome.table[self.dbset].get_database(
            #    ).DestroyRecordSet(self.recordset)
            self.recordset = None

    def get_cursor(self):
        """Create and return cursor on this datasource's recordset."""
        if self.recordset:
            cursor = self.dbhome.create_recordset_cursor(
                self.dbset, self.dbname, self.recordset
            )
        else:
            cursor = self.dbhome.create_recordset_cursor(
                self.dbset, self.dbname, self.dbhome.recordlist_nil(self.dbset)
            )
        return cursor

    def join_field_occurrences(self, record, field):
        """Return concatenated occurrences of field.

        The record value, a repr(<python object>), is held as multiple
        occurrences of a field in a record on a DPT file.  Each occurrence is
        a maximum of 256 bytes (in Python terminology) so a Python object is
        split into multiple occurrences of a field for storage.
        """
        i = 1
        values = []
        while record.GetFieldValue(field, self._fieldvalue, i):
            values.append(self._fieldvalue.ExtractString())
            i += 1
        return "".join(values)

    def set_recordset(self, records):
        """Set records as this datasource's recordset."""
        # if self.recordset:
        #    self.dbhome.get_table_connection(
        #        self.dbset).DestroyRecordSet(self.recordset)
        self.recordset = records
