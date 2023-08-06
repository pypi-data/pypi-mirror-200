import time
from unittest.mock import patch
import httpx
import respx

from chaoslib.run import EventHandlerRegistry
from chaosreliably.activities.safeguard.probes import call_endpoint
from chaosreliably.controls.prechecks import configure_control as precheck
from chaosreliably.controls.safeguard import configure_control as safeguard


@respx.mock
@patch("chaosaddons.controls.safeguards.exit_gracefully", autospec=True)
def test_prechecks_run_interrupts_execution(exit_gracefully):
    url = "https://example.com/try-me"

    m = respx.get(url).mock(return_value=httpx.Response(
        200, json={"ok": False, "error": "boom"})
    )
    
    registry = EventHandlerRegistry()
    experiment = {
        "title": "an experiment",
        "description": "n/a",
        "method": []
    }
    journal = {}

    precheck(registry, url)

    try:
        registry.started(experiment, journal)
    finally:
        registry.finish(journal)

    respx.calls.assert_called_once()
    assert registry.handlers[0].guardian.interrupted is True


@respx.mock
def test_safeguard_expects_a_200():
    url = "https://example.com/try-me"

    respx.get(url).mock(return_value=httpx.Response(400))
    assert call_endpoint(url) is False

    respx.get(url).mock(return_value=httpx.Response(200, json={"ok": True}))
    assert call_endpoint(url) is True


@respx.mock
def test_safeguard_not_ok_expects_error_message():
    url = "https://example.com/try-me"

    respx.get(url).mock(return_value=httpx.Response(400))
    assert call_endpoint(url) is False

    respx.get(url).mock(return_value=httpx.Response(200, json={
        "ok": False,
        "error": "boom"
    }))
    assert call_endpoint(url) is False


@respx.mock
@patch("chaosaddons.controls.safeguards.exit_gracefully", autospec=True)
def test_prechecks_run_once(exit_gracefully):
    url = "https://example.com/try-me"

    m = respx.get(url).mock(return_value=httpx.Response(200, json={"ok": True}))
    
    registry = EventHandlerRegistry()
    experiment = {
        "title": "an experiment",
        "description": "n/a",
        "method": []
    }
    journal = {}

    precheck(registry, url)

    try:
        registry.started(experiment, journal)
    finally:
        registry.finish(journal)

    respx.calls.assert_called_once()
    assert registry.handlers[0].guardian.interrupted is False


@respx.mock
@patch("chaosaddons.controls.safeguards.exit_gracefully", autospec=True)
def test_safeguard_run_periodically(exit_gracefully):
    url = "https://example.com/try-me"

    m = respx.get(url).mock(return_value=httpx.Response(200, json={"ok": True}))
    
    registry = EventHandlerRegistry()
    experiment = {
        "title": "an experiment",
        "description": "n/a",
        "method": []
    }
    journal = {}

    safeguard(registry, url, 0.5)

    try:
        registry.started(experiment, journal)
        time.sleep(2.0)
    finally:
        registry.finish(journal)

    assert respx.calls.call_count > 1
    assert registry.handlers[0].guardian.interrupted is False


@respx.mock
@patch("chaosaddons.controls.safeguards.exit_gracefully", autospec=True)
def test_safeguard_run_interrupts_execution(exit_gracefully):
    url = "https://example.com/try-me"

    m = respx.get(url).mock(side_effect=[
        httpx.Response(200, json={"ok": True}),
        httpx.Response(200, json={"ok": False, "error": "boom"}),
        httpx.Response(200, json={"ok": False, "error": "boom"}),
        httpx.Response(200, json={"ok": False, "error": "boom"})
    ])
    
    registry = EventHandlerRegistry()
    experiment = {
        "title": "an experiment",
        "description": "n/a",
        "method": []
    }
    journal = {}

    safeguard(registry, url, 0.5)

    try:
        registry.started(experiment, journal)
        time.sleep(2.0)
    finally:
        registry.finish(journal)

    assert respx.calls.call_count > 1
    assert registry.handlers[0].guardian.interrupted is True


@respx.mock
@patch("chaosaddons.controls.safeguards.exit_gracefully", autospec=True)
def test_safeguard_can_be_many(exit_gracefully):
    url = "https://example.com/try-me"

    m = respx.get(url).mock(side_effect=[
        httpx.Response(200, json={"ok": True}),
        httpx.Response(200, json={"ok": False, "error": "boom"}),
        httpx.Response(200, json={"ok": False, "error": "boom"}),
        httpx.Response(200, json={"ok": False, "error": "boom"})
    ])
    
    url2 = "https://example.com/try-me-as-well"

    m = respx.get(url2).mock(side_effect=[
        httpx.Response(200, json={"ok": True}),
        httpx.Response(200, json={"ok": True}),
        httpx.Response(200, json={"ok": True}),
        httpx.Response(200, json={"ok": True}),
    ])
    
    registry = EventHandlerRegistry()
    experiment = {
        "title": "an experiment",
        "description": "n/a",
        "method": []
    }
    journal = {}

    safeguard(registry, url, 0.5)
    safeguard(registry, url2, 0.5)

    try:
        registry.started(experiment, journal)
        time.sleep(2.0)
    finally:
        registry.finish(journal)

    assert respx.calls.call_count > 1
    assert registry.handlers[0].guardian.interrupted is True

    assert respx.calls.call_count > 1
    assert registry.handlers[1].guardian.interrupted is False
