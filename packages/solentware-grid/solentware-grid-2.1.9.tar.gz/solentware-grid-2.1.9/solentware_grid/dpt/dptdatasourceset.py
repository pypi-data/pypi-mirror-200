# dptdatasourceset.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide bsddb style access to a list of DPT record sets and lists.

Each record set in the list is displayed in record number order but the
records will not appear in an obvious sort order like alphabetical.  There
will be an application specific reason for the list of record sets to be in
the given order.

Typical use is:
Find the records that match each of the forenames initials and surname in a
given name.  Build sets that match as many as possible of the name elements
and display the reords with those that match most at start.

See www.dptoolkit.com for details of DPT.

"""

from dptdb import dptapi

from ..core.dataclient import DataSource


class DataSourceSet(DataSource):
    """Define an interface between a database and GUI controls.

    The database is an instance of a subclass of dptapi.DPTapi.

    """

    def __init__(self, dbhome, dbset, dbname, newrow=None):
        """Define an interface between DPT database and GUI controls.

        See superclass for description of arguments.

        """
        super().__init__(dbhome, dbset, dbname, newrow=newrow)

        self.key_sets = []
        self.recordsets = dict()
        # self.partial_keys = dict()
        # self._fieldvalue = dptapi.APIFieldValue()

    def close(self):
        """Close resources."""
        self._clear_recordsets()

    def get_cursor(self):
        """Return cursor on record set, or list, associated with datasource."""
        if self.recordsets:
            return self.dbhome.create_recordsetlist_cursor(
                self.dbset,
                self.dbname,
                keyrange=None,
                recordset=self.recordsets,
            )
        dbfile = self.dbhome.get_table_connection(self.dbset)
        empty = dbfile.CreateRecordList()
        return self.dbhome.create_recordsetlist_cursor(
            self.dbset, self.dbname, keyrange=None, recordset={None: empty}
        )

    def get_recordset(self, dbname, key=None, from_=None):
        """Create a recordset of records with key==key.

        dbname: secondary (index) used to partition records
        key: find records with value key on dbname
        When key=None find all records in from_
        from_: find records in record set from_ or record list from_.
        When from_=None find from all records in file.
        """
        if key is None:
            if from_ is None:
                return self._find_all_records()
            return self._in_recordset_find(dbname, from_)
        if from_ is None:
            return self._find_field_equals_value(dbname, key)
        return self._in_recordset_field_equals_value(dbname, from_, key)

    def set_recordsets(
        self,
        dbname,
        partial_keys=None,
        constant_keys=None,
        include_without_constant_keys=False,
        population=None,
    ):
        """Create all combinations of partial keys.

        dbname: secondary (index) containing partial key values
        partial_keys: all combinations used as a partial key
        constant_keys: values added to each combintion
        include_without_constant_keys: all combinations without constant_keys
        added, as well, if True
        population: subset of records to partition by partial_keys.  Use all
        records if None
        """

        def set_partial_keys(
            partial, constant, new, old, add_without_constant=False
        ):
            include_constant = [constant]
            if add_without_constant:
                include_constant.append(set())
            for k in include_constant:
                for j in new:
                    new_without_j = new.copy()
                    new_without_j.remove(j)
                    old_with_j = k.union(old)
                    old_with_j.add(j)
                    partial.add(tuple(sorted(old_with_j)))
                    if new_without_j:
                        set_partial_keys(
                            partial,
                            constant,
                            new_without_j,
                            old_with_j,
                            add_without_constant,
                        )

        if partial_keys is None:
            partial_keys = set()
        if constant_keys is None:
            constant_keys = set()
        combinations = set()
        set_partial_keys(
            combinations,
            constant_keys,
            partial_keys,
            set(),
            add_without_constant=include_without_constant_keys,
        )

        dpn = []
        for pnc in combinations:
            pns = set(pnc)
            dpn.append(
                (
                    len(constant_keys)
                    != len([n for n in constant_keys if n in pns]),
                    -len([n for n in pnc if len(n) > 1]),
                    -len(pnc),
                    pnc,
                )
            )
        self.key_sets = [pk[-1] for pk in sorted(dpn)]

        self._clear_recordsets()

        dbfile = self.dbhome.get_table_connection(self.dbset)
        dbindex = self.dbhome.table[self.dbset].secondary[dbname]
        all_records = self.get_recordset(
            dbindex, from_=population
        )  # should be fd not fdwol
        unmatched_records = dbfile.CreateRecordList()
        unmatched_records.Place(all_records)
        for keyset in self.key_sets:
            foundset = unmatched_records
            for k in keyset:
                onfoundset = foundset
                foundset = self._in_recordset_field_equals_value(
                    dbindex, onfoundset, k
                )
                if onfoundset is not unmatched_records:
                    dbfile.DestroyRecordSet(onfoundset)
            if foundset is not unmatched_records:
                unmatched_records.Remove(foundset)
            if foundset.Count():
                self.recordsets[keyset] = foundset
            elif foundset is not unmatched_records:
                dbfile.DestroyRecordSet(foundset)
        if unmatched_records.Count():
            self.recordsets[None] = unmatched_records
            self.key_sets.append(None)
        dbfile.DestroyRecordSet(all_records)
        self.key_sets = [ks for ks in self.key_sets if ks in self.recordsets]

    def _clear_recordsets(self):
        """Destroy Record Sets."""
        dbfile = self.dbhome.get_table_connection(self.dbset)
        for recordset in self.recordsets.values():
            dbfile.DestroyRecordSet(recordset)
        self.recordsets.clear()

    def _find_all_records(self):
        """Return APIFoundset containing all records on DPT file."""
        dbfile = self.dbhome.get_table_connection(self.dbset)
        return dbfile.FindRecords()

    def _find_field_equals_value(self, dbname, value):
        """Return APIFoundset from foundset where fieldname contains value.

        value: field value
        """
        dbfile = self.dbhome.get_table_connection(self.dbset)
        # dbname = self.dbhome.table[self.dbset].secondary[self.dbname]
        return dbfile.FindRecords(
            dptapi.APIFindSpecification(
                dbname,  # 'Playerpartialname',  # self.dbname,
                dptapi.FD_EQ,
                dptapi.APIFieldValue(value),
            )
        )

    def _in_recordset_find(self, dbname, recordset):
        """Return APIFoundset containing all records on DPT file."""
        dbfile = self.dbhome.get_table_connection(self.dbset)
        # dbname = self.dbhome.table[self.dbset].secondary[self.dbname]
        return dbfile.FindRecords(
            dptapi.APIFindSpecification(
                dbname,  # 'Playerpartialname',  # self.dbname,
                dptapi.FD_ALLRECS,
                dptapi.APIFieldValue(""),
            ),
            recordset,
        )

    def _in_recordset_field_equals_value(self, dbname, recordset, value):
        """Return APIFoundset from foundset where fieldname contains value.

        recordset: DPT foundset or list.
        value: field value
        """
        dbfile = self.dbhome.get_table_connection(self.dbset)
        # dbname = self.dbhome.table[self.dbset].secondary[self.dbname]
        return dbfile.FindRecords(
            dptapi.APIFindSpecification(
                dbname,  # 'Playerpartialname',  # self.dbname,
                dptapi.FD_EQ,
                dptapi.APIFieldValue(value),
            ),
            recordset,
        )
