import pytest

from ..domain.directory import TransientDirectory
from ..domain.directory.exceptions import DirectoryException, DIRECTORY_CONTACT_NOT_FOUND_ERROR_MESSAGE, \
    DIRECTORY_DUPLICATED_CONTACT_ERROR_MESSAGE
from ..domain.models import Contact


@pytest.fixture
def unknown_contact():
    return Contact(name="unknown", phone="123456789")


@pytest.fixture
def example_contact_name():
    return "jarvis"


@pytest.fixture
def example_contact(example_contact_name):
    return Contact(name=example_contact_name, phone="1512345678")


@pytest.fixture
def duplicated_contact(example_contact_name):
    return Contact(name=example_contact_name, phone="123456789")


@pytest.fixture
def transient_directory(example_contact):
    ds = TransientDirectory()
    ds.add(example_contact)
    yield ds


def test_directory_cannot_retrieve_not_existing_contact(transient_directory, unknown_contact):
    with pytest.raises(DirectoryException, match=DIRECTORY_CONTACT_NOT_FOUND_ERROR_MESSAGE):
        transient_directory.query(unknown_contact.name)


def test_directory_can_retrieve_added_contact(transient_directory, example_contact):
    assert transient_directory.query(example_contact.name) == example_contact


def test_directory_cannot_add_duplicated_contact(transient_directory, duplicated_contact):
    with pytest.raises(DirectoryException, match=DIRECTORY_DUPLICATED_CONTACT_ERROR_MESSAGE):
        transient_directory.add(duplicated_contact)


def test_directory_cannot_remove_not_existing_contact(transient_directory, unknown_contact):
    with pytest.raises(DirectoryException, match=DIRECTORY_CONTACT_NOT_FOUND_ERROR_MESSAGE):
        transient_directory.remove(unknown_contact.name)


def test_directory_can_remove_existing_contact(transient_directory, example_contact):
    transient_directory.remove(example_contact.name)
    with pytest.raises(DirectoryException, match=DIRECTORY_CONTACT_NOT_FOUND_ERROR_MESSAGE):
        transient_directory.query(example_contact.name)
