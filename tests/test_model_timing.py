"""Timing diagnostics are bounded and cannot retain HTTP trace secrets."""

import json

from ppm_api.model_timing import EVENTS, TransportTiming


async def test_transport_timing_keeps_only_known_monotonic_offsets(monkeypatch):
    clock = [100.0]
    monkeypatch.setattr("ppm_api.model_timing.perf_counter", lambda: clock[0])
    timing = TransportTiming()
    clock[0] = 100.125
    await timing.trace("connection.start_tls.complete", {"headers": "secret", "body": "private"})
    await timing.trace("private-unknown-event", {"secret": "never retain"})
    assert timing.events == {"connection.start_tls.complete": 125}
    clock[0] = 122.0
    await timing.trace("http11.receive_response_headers.failed", {"exception": "sensitive"})
    assert timing.events["http11.receive_response_headers.failed"] == 22000
    assert set(timing.events) <= EVENTS
    assert "secret" not in json.dumps(timing.events)
    assert "private" not in json.dumps(timing.events)
