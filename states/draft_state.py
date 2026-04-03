# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Draft State
# Jonathan Principato (400527847)

from states.schedule_state import ScheduleState


# Design Pattern: State
# Is the initial state of every schedule
# Drafts can only transition to published

class DraftState(ScheduleState):
    def __init__(self, schedule_id, schedule_repo, shift_repo):
        super().__init__(schedule_id, schedule_repo, shift_repo)

    def publish(self):
        shifts = self._shift_repo.get_shifts_by_schedule_id(self._schedule_id)
        if not shifts:
            raise ValueError("Cannot Publish schedule with no shifts")
        
        self._schedule_repo.update_state(self._schedule_id, "published")

    def complete(self):
        raise ValueError("Cannot change state from draft to complete")

