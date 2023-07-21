class OPDocumentFile(dict):
    def __init__(self, file_dict):
        super().__init__(file_dict)

    @property
    def file_id(self) -> str:
        return self["id"]

    @property
    def name(self) -> str:
        return self["name"]

    @property
    def size(self) -> int:
        return self["size"]

    @property
    def content_path(self) -> str:
        return self["content_path"]
