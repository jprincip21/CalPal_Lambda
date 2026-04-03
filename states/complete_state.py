# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Complete State
# Jonathan Principato (400527847)

from states.schedule_state import ScheduleState


# Design Pattern: State
# Complete Is the final state of every schedule
# Cannot transition back to published or draft

class CompleteState(ScheduleState):
    def __init__(self, schedule_id, schedule_repo, shift_repo):
        super().__init__(schedule_id, schedule_repo, shift_repo)

    def publish(self):
        raise ValueError("Cannot Publish a completed scheudle")
    
    def complete(self):
        raise ValueError("Cannot complete a completed scheudle")