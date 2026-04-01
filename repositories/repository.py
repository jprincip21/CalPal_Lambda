# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Repository Pattern
# Jonathan Principato (400527847)

from abc import ABC, abstractmethod

# Abstract Repository Class - Repository Pattern
# Defines the interface that all concrete repositories must implement
class Repository(ABC):
    def __init__(self, db):
        self.db = db

    # Remove if stays unused
    @abstractmethod
    def get(self, id):
        """Retrieve a single entity by id"""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all entities"""
        pass

    @abstractmethod
    def create(self, entity):
        """Create a new entity in the database"""
        pass

    @abstractmethod
    def update(self, entity):
        """Update an existing entity in the database"""
        pass

    @abstractmethod
    def delete(self, id):
        """Delete an entity by id from the database"""
        pass