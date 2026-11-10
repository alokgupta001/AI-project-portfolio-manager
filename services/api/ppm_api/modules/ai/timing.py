"""Monotonic transport milestones containing no request, response or trace info."""

from time import perf_counter

EVENTS = {
    f"{prefix}.{phase}.{state}"
    for prefix, phases in (
        ("connection", ("connect_tcp", "start_tls")),
        (
            "http11",
            (
                "send_request_headers",
                "send_request_body",
                "receive_response_headers",
                "receive_response_body",
            ),
        ),
    )
    for phase in phases
    for state in ("started", "complete", "failed")
}


class TransportTiming:
    def __init__(self) -> None:
        """Start a bounded dictionary of safe timing offsets for one adapter attempt."""
        self.started = perf_counter()
        self.events: dict[str, int] = {}

    async def trace(self, name: str, info: dict) -> None:
        """Discard trace info entirely: it can include credentials and private payloads."""
        if name in EVENTS:
            self.events[name] = max(0, int((perf_counter() - self.started) * 1000))
