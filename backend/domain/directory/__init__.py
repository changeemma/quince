from abc import ABC, abstractmethod

from .exceptions import DirectoryException, DIRECTORY_DUPLICATED_CONTACT_ERROR_MESSAGE, \
    DIRECTORY_CONTACT_NOT_FOUND_ERROR_MESSAGE
from ..models import Contact


class Directory(ABC):
    @abstractmethod
    def add(self, contact: Contact) -> Contact:
        pass

    @abstractmethod
    def query(self, contact_name: str) -> Contact | None:
        pass

    @abstractmethod
    def remove(self, contact_name: str) -> None:
        pass


class TransientDirectory(Directory):
    def __init__(self):
        self.contacts = set()

    def add(self, contact: Contact) -> Contact:
        if contact in self.contacts:
            raise DirectoryException(DIRECTORY_DUPLICATED_CONTACT_ERROR_MESSAGE)
        self.contacts.add(contact)
        return contact

    def query(self, contact_name: str, *, strict: bool = True) -> Contact | None:
        for contact in self.contacts:
            if contact.name == contact_name:
                return contact
        if not strict:
            return None
        raise DirectoryException(DIRECTORY_CONTACT_NOT_FOUND_ERROR_MESSAGE)

    def remove(self, contact_name: str, *, strict: bool = True) -> None:
        contact = self.query(contact_name, strict=strict)
        if contact:
            self.contacts.remove(contact)
