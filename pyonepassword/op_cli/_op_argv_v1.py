from ._op_argv_base import _OPArgvBase
from ..op_items._op_items_base import OPAbstractItem
from ..py_op_exceptions import OPInvalidItemException


class _OPArgv(_OPArgvBase):

    @classmethod
    def get_verify_signin_argv(cls, op_exe):
        argv = ["templates"]
        argv_obj = cls(op_exe, "list", argv)
        return argv_obj

    @classmethod
    def get_generic_argv(cls, op_exe, get_subcommand, obj_identifier, sub_cmd_args):
        args = [obj_identifier]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe, "get", args, subcommand=get_subcommand)
        return argv

    @classmethod
    def get_item_argv(cls, op_exe, item_name_or_uuid, vault=None, fields=None):
        sub_cmd_args = []
        if vault:
            sub_cmd_args.extend(["--vault", vault])

        if fields:
            sub_cmd_args.extend(["--fields", fields])
        argv = cls.get_generic_argv(
            op_exe, "item", item_name_or_uuid, sub_cmd_args)
        return argv

    @classmethod
    def get_totp_argv(cls, op_exe, item_name_or_uuid, vault=None):
        sub_cmd_args = []
        if vault:
            sub_cmd_args.extend(["--vault", vault])

        argv = cls.get_generic_argv(
            op_exe, "totp", item_name_or_uuid, sub_cmd_args)
        return argv

    @classmethod
    def get_document_argv(cls, op_exe, document_name_or_uuid, vault=None):
        sub_cmd_args = []
        if vault:
            sub_cmd_args.extend(["--vault", vault])
        argv = cls.get_generic_argv(
            op_exe, "document", document_name_or_uuid, sub_cmd_args)
        return argv

    @classmethod
    def create_item_argv(cls, op_exe, item: OPAbstractItem, item_name: str, vault: str = None, encoding="utf-8"):
        if not item.is_from_template:
            raise OPInvalidItemException(
                f"Attempting to create item using object not from a template: {item_name}")
        template_filename = item.details_secure_tempfile(
            encoding=encoding)

        category = item.category
        url = item.first_url()

        return cls._create_item_argv(op_exe, template_filename, item_name, url=url, category=category, vault=vault, encoding=encoding)

    @classmethod
    def _create_item_argv(cls, op_exe, template_filename, item_name, url=None, category=None, vault: str = None, encoding="utf=8"):
        # unfortunately the 'op' command can only set one URL
        # so we need to get only the first one

        argv = [category, "--title", item_name,
                "--template", template_filename]
        url_value = None

        if url:
            url_value = url.url
        if url_value:
            argv.extend(["--url", url_value])

        if vault:
            argv.extend(["--vault", vault])

        return cls(op_exe, "create", argv, subcommand="item")

    @classmethod
    def forget_argv(cls, op_exe, account_shorthand):
        forget_args = [account_shorthand]
        argv = cls(op_exe, "forget", forget_args)
        return argv

    @classmethod
    def list_generic_argv(cls, op_exe, list_subcommand, sub_command_args):
        argv = cls(op_exe, "list", sub_command_args,
                   subcommand=list_subcommand)
        return argv

    @classmethod
    def list_items_argv(cls, op_exe, categories=[], include_archive=False, tags=[], vault=None):
        list_items_args = []
        if categories:
            categories_arg = ",".join(categories)
            list_items_args.extend(["--categories", categories_arg])
        if include_archive:
            list_items_args.append("--include-archive")
        if tags:
            tags_args = ",".join(tags)
            list_items_args.extend(["--tags", tags_args])
        if vault:
            list_items_args.extend(["--vault", vault])

        argv = cls.list_generic_argv(op_exe, "items", list_items_args)
        return argv
