import re
from enum import Enum


class OPFieldTypeEnum(Enum):
    PASSWORD = "password"
    TEXT = "text"
    URL = "url"
    DELETE = "delete"


class _OPFieldAssignment(str):
    FIELD_TYPE: OPFieldTypeEnum = None

    def __new__(cls, field_label: str, value: str, * args, section_label: str = None, **kwargs):
        if cls.FIELD_TYPE is None:
            raise TypeError(
                f"{cls.__name__} must be extended and FIELD_TYPE set")
        assignment_str = ""
        field_label = cls._field_assignment_escape(field_label)
        field_type_string = cls.FIELD_TYPE.value
        if section_label:
            section_label = cls._field_assignment_escape(section_label)
            assignment_str = f"{section_label}."

        assignment_str += f"{field_label}[{field_type_string}]"

        assignment_str = cls._process_value_str(assignment_str, value)

        return super().__new__(cls, assignment_str)

    @classmethod
    def _process_value_str(cls, assignment_str, value):
        # HACK: We need to override this in OPFieldAssignmentDelete
        # so we can raise an exception is an actual value is passed in

        # intentionally not using string formatting to assign value
        # in some cases value will be a RedactedString, so concatenation
        # will prevent it from self-redacting
        assignment_str += "=" + value
        return assignment_str

    @classmethod
    def _field_assignment_escape(cls, input_string):

        pattern = r"([.=\\])"
        repl = r"\\\1"
        escaped_string = re.sub(pattern, repl, input_string)
        return escaped_string


class OPFieldAssignmentPassword(_OPFieldAssignment):
    FIELD_TYPE = OPFieldTypeEnum.PASSWORD

    def __init__(self, *args, **kwargs):
        super().__init__()
        redacted = self._redact()
        self._redacted_assignment = redacted

    def __str__(self):
        # NOTE: this is only intended to affect printing/logging of this string
        # It DOES NOT make `op item edit` operations more secure. The cleartext password assignment
        # is still passed as an argument and visible to other processes
        return self._redacted_assignment

    def _redact(self):
        lhs, rhs = self.rsplit("=", maxsplit=1)
        mask = "*" * len(rhs)

        # introduce an intentional syntax error here
        # in case we try to use this redacted string as the actual
        # assignment during execution
        # This should generate an error
        # we don't want to accidentaly set someone's password
        # to "*************"
        # this is an equals emoji rather than an equals sign
        redacted = f"{lhs}🟰{mask}"
        return redacted


class OPFieldAssignmentText(_OPFieldAssignment):
    FIELD_TYPE = OPFieldTypeEnum.TEXT


class OPFieldAssignmentURL(_OPFieldAssignment):
    FIELD_TYPE = OPFieldTypeEnum.URL


class OPFieldAssignmentDelete(_OPFieldAssignment):
    FIELD_TYPE = OPFieldTypeEnum.DELETE

    def __new__(cls, field_label: str, *args, section_label: str = None, **kwargs):
        # pass None in for value arg
        value = None
        obj = super().__new__(cls, field_label, value, *args,
                              section_label=section_label, **kwargs)
        return obj

    @classmethod
    def _process_value_str(cls, assignment_str, _value):
        # This is kind of a hack
        # "delete" assignment strings can't have a value
        # so we're overriding this method
        # and raising an exception if we were passed a value
        if _value:
            raise ValueError(
                "Field assignment value not allowed for OPFieldAssignmentDelete")
        return assignment_str


FIELD_TYPE_MAP = {
    OPFieldTypeEnum.DELETE: OPFieldAssignmentDelete,
    OPFieldTypeEnum.PASSWORD: OPFieldAssignmentPassword,
    OPFieldTypeEnum.TEXT: OPFieldAssignmentText,
    OPFieldTypeEnum.URL: OPFieldAssignmentURL,
}
