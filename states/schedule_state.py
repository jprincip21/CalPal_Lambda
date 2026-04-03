# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Schedule State
# Jonathan Principato (400527847)

from abc import ABC, abstractmethod

# Design Pattern: State Pattern
# Abstract State base class for all states (draft, published, complete)
# Defines the interface that all concrete states must implement
# Concrete States will have handle methods which handle what happens on transition

class ScheduleState(ABC):
    def __init__(self, schedule_id, schedule_repo, shift_repo):
        self._schedule_id = schedule_id
        self._schedule_repo = schedule_repo
        self._shift_repo = shift_repo

    @abstractmethod
    def publish(self):
        """Change schedule to published state"""
        pass

    @abstractmethod
    def complete(self):
        """Change schedule to complete state"""
        pass

    @abstractmethod
    def get_current_state(self):
        """Returns the current schedule state"""
        pass
