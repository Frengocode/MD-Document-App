from fastapi import HTTPException


class EmptyReasonException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Reason should be !")


class SaveDocumentException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Can't save Document")


class DocumentNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Document not found")
