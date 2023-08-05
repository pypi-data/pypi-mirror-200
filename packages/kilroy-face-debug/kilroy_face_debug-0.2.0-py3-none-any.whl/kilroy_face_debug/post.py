from typing import Optional
from uuid import UUID

from kilroy_face_py_shared import SerializableModel


class PostTextData(SerializableModel):
    content: str


class PostImageData(SerializableModel):
    raw: str
    filename: Optional[str]


class PostData(SerializableModel):
    text: Optional[PostTextData]
    image: Optional[PostImageData]


class Post(SerializableModel):
    data: PostData
    id: UUID
