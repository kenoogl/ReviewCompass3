"""セッションログの追記専用更新と変更検知。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class UpdateResult:
  action: str
  events: tuple
  appended: tuple


def merge_append_only(existing, incoming) -> UpdateResult:
  existing_events = tuple(existing)
  incoming_events = tuple(incoming)

  if incoming_events == existing_events:
    return UpdateResult(
      action="unchanged",
      events=existing_events,
      appended=(),
    )
  if not existing_events:
    return UpdateResult(
      action="created",
      events=incoming_events,
      appended=incoming_events,
    )
  if incoming_events[:len(existing_events)] == existing_events:
    return UpdateResult(
      action="updated",
      events=incoming_events,
      appended=incoming_events[len(existing_events):],
    )
  return UpdateResult(
    action="preserved",
    events=existing_events,
    appended=(),
  )
