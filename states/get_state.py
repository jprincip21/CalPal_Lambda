from states.draft_state import DraftState
from states.published_state import PublishedState
from states.complete_state import CompleteState

# Factory Pattern: Creates a certain type of state object based on requested state
def get_state(state: str, schedule_id: int, schedule_repo, shift_repo):
    if state == "published":
        return PublishedState(schedule_id, schedule_repo, shift_repo)
    elif state == "complete":
        return CompleteState(schedule_id, schedule_repo, shift_repo)
    else:
        return DraftState(schedule_id, schedule_repo, shift_repo)