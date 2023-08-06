from uuid import uuid4, UUID
import json
import re


def gid():
    return str(uuid4())


def maybe_gid(possible_gid):
    possible_gid = str(possible_gid)
    try:
        possible_uuid = UUID(possible_gid, version=4)
    except ValueError:
        return False
    return str(possible_uuid) == possible_gid


class make_object:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


def field_title(field, language):
    title = field.label[language]
    if field.unit:
        title += f" [{field.unit}]"
    return title


def test_false(data):
    return str(data).lower().strip() in (
        "",
        "0",
        "no",
        "n",
        "off",
        "false",
        "f",
        "unchecked",
        "deselected",
        "none",
        "null",
        "undefined",
    )


def test_true(data):
    return not test_false(data)


class FieldColumns:
    """FieldColumns are needed for class fields, that have nested subfields.

    With FieldColumns, we can flatten a list of fields to a list of columns,
    associated with those fields.

    Each column has a fieldstack, that is a list of the field and nested subfields.
    For a regular field, the fieldstack is just that field.
    A classfield with three subfields will yield three columns, and each column has
    a fieldstack with the classfield first, and then the subfield for that column.
    If that subfield is another classfield, we'll get more columns and deeper
    stackfields.

    Most of the time, you won't need the stackfield in the client code, see also the
    _FieldColumn implementation where we get the 'name' for a column by walking the
    fieldstack.

    Client code can look something like this, for reading from Unicat:

    ```
    columns = FieldColumns(fields, prefix_column_count=3)
    for column in columns:
        column_name = column.name()  # e.g. 'image' or 'dimensions.width__mm'
        column_label = column.label()  # e.g. 'Image' or 'Dimensions\nWidth [mm]'
        column_value = None
        error = None
        try:
            column_value = column.extract_value(record.fields[language])
        except KeyError:
            error = (
                "Field is not part of this definition. Do not enter data here."
            )
    ```

    FieldColumns can also be used to write to Unicat, when we need a record's fields
    data structure:

    ```
    recordfields_data = {}
    for column in columns:
        fieldvalue = row[column.index].value
        column.update_fields_data(recordfields_data, fieldvalue)
    unicat.update_record(gid, language, recordfields_data)
    ```
    """

    def __init__(self, fields, prefix_column_count=0):
        self._columns = []
        index = prefix_column_count
        for fieldstack in self._flatten_fields(fields, []):
            self._columns.append(_FieldColumn(index, fieldstack))
            index += 1
        self._iterindex = 0

    def __iter__(self):
        self._iterindex = 0
        return self

    def __next__(self):
        if self._iterindex >= len(self._columns):
            raise StopIteration
        column = self._columns[self._iterindex]
        self._iterindex += 1
        return column

    def _flatten_fields(self, fields, fieldstack):
        flattened_fields = []
        for field in fields:
            if field.type == "class":
                subfieldstack = [*fieldstack, field]
                for subfield in self._flatten_fields(
                    field.class_.fields, subfieldstack
                ):
                    flattened_fields.append(subfield)
            else:
                flattened_fields.append([*fieldstack, field])
        return flattened_fields


class _FieldColumn:
    def __init__(self, index, fieldstack):
        self.index = index
        self.number = index + 1
        self._fieldstack = fieldstack

    def name(self, separator="."):
        return separator.join(field.name for field in self._fieldstack)

    def label(self, language, separator="\n"):
        return separator.join(
            field_title(field, language) for field in self._fieldstack
        )

    def extract_value(self, localized_record_fields):
        """Going to Excel (or csv), extract a value from a record to put in the column.

        Don't provide column data, provide the row record.fields[language]

        ```
        for column in columns:
            columnvalue = None
            try:
                columnvalue = column.extract_value(record.fields[language])
            except KeyError:
                comment = (
                    "Field is not part of this definition. Do not enter data here."
                )
        ```
        """
        field_value = localized_record_fields  # initial reference
        for entry in self._fieldstack:
            field_value = field_value[entry.name]  # may raise KeyError
            if not field_value:
                break
        return field_value.value if field_value else None

    def update_fields_data(self, localized_record_fields_data, value):
        """Coming from Excel (or csv), build fields_data for a record from each column.

        Updates the localized_record_fields_data argument.

        localized_record_fields_data looks like record.fields[language], but as a
        json data structure
        localized_record_fields_data starts with a single {}
        value is the value in the cell

        ```
        fields_data = {}
        for column in columns:
            value = row[column.index].value
            column.update_fields_data(fields_data, value)
        unicat.update_record(gid, language, fields_data)
        ```
        """
        field_data = convert_value_to_fielddata(self.field.type, value)
        for entry in reversed(self._fieldstack):
            temp = {entry.name: field_data}
            field_data = temp
        merge_dicts(localized_record_fields_data, field_data)

    @property
    def field(self):
        return self._fieldstack[-1]

    @property
    def fieldstack(self):
        return self._fieldstack


def make_bool(any):
    """
    bool("False") returns true, make_bool("False") doesn't
    """
    if any is None:
        return None
    return test_true(any)


def make_str(any):
    if any is None or len(any) == 0:
        return None
    if isinstance(any, list):
        return "\n".join(str(line) for line in any)  # normalizes newlines
    return "\n".join(str(any).splitlines())  # normalizes newlines


def make_int(any):
    if any is None:
        return None
    return int(any)


def make_float(any):
    if any is None:
        return None
    return float(any)


def noop(any):
    return any


def make_str_list(any):
    if any is None or len(any) == 0:
        return None
    if not isinstance(any, list):
        any = str(any).splitlines()
    return [str(line).strip() for line in any]  # each entry must be a string


VALUE_TO_FIELDDATA = {
    "text": make_str,
    "textline": make_str,
    "textlist": make_str_list,
    "number": make_int,
    "decimal": make_float,
    "boolean": make_bool,
    "code": make_str,
    "barcode": make_str,
    "class": noop,  # let it burn -- we shouldn't update records with json data
    "classlist": noop,  # let it burn -- we shouldn't update records with json data
    "image": make_str,
    "imagelist": make_str_list,
    "file": make_str,
    "filelist": make_str_list,
    "record": make_str,
    "recordlist": make_str_list,
    "fieldpicker": make_str,
}

FIELDDATA_TO_VALUE = {
    "text": make_str,
    "textline": make_str,
    "textlist": make_str,
    "number": noop,
    "decimal": noop,
    "boolean": noop,
    "code": make_str,
    "barcode": make_str,
    "class": make_str,
    "classlist": make_str,
    "image": make_str,
    "imagelist": make_str,
    "file": make_str,
    "filelist": make_str,
    "record": make_str,
    "recordlist": make_str,
    "fieldpicker": make_str,
}


def convert_value_to_fielddata(fieldtype, value):
    """Return a value suitable for writing to Unicat, for list field types this
    means converting newline-separated entries to lists.
    """
    return VALUE_TO_FIELDDATA[fieldtype](value)


def convert_fielddata_to_value(fieldtype, fielddata):
    """Return a value suitable for writing in a cell, such as a text or a number.
    Lists will be flattened by stringifying each item and concatenating with \n.
    """
    return FIELDDATA_TO_VALUE[fieldtype](fielddata)


def merge_dicts(a, b):
    """Merge b into a, returning a.

    a is updated; if you don't want to mutate a, call it as `merge_dicts(dict(a), b)`.
    """
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(a[key], b[key])
            else:
                a[key] = b[key]  # overwrite a
        else:
            a[key] = b[key]
    return a


def hash_text(text):  # unicode ok
    hash = 0
    for letter in text:
        hash = (31 * hash + ord(letter)) & 0xFFFFFFFF
    hash = ((hash + 0x80000000) & 0xFFFFFFFF) - 0x80000000
    return ("00000000" + hex(hash)[2:])[-8:]


def hash_data(data):
    return hash_text(json.dumps(data))
