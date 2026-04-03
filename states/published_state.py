# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Published State
# Jonathan Principato (400527847)

from states.schedule_state import ScheduleState


# Design Pattern: State
# Published Schedules can only transition to Complete

class PublishedState(ScheduleState):
    def __init__(self, schedule_id, schedule_repo, shift_repo):
        super().__init__(schedule_id, schedule_repo, shift_repo)

    def publish(self):
        raise ValueError("Cannot Publish a schedule that is already published.")
    
    def complete(self):
        self._schedule_repo.update_state(self._schedule_id, "complete")
