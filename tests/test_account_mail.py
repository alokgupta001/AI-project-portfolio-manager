"""Account messages and SMTP boundaries; no network or live recipient is used."""

import smtplib
from uuid import uuid4

import pytest
from ppm_api.account_mail import account_message, smtp_delivery
from ppm_api.config import Settings, load_settings
from ppm_api.identity import delivery_instructions
from pydantic import SecretStr, ValidationError


def smtp_settings(settings):
    return settings.model_copy(
        update={
            "mail_mode": "smtp",
            "smtp_host": "smtp.example.com",
            "smtp_user": "test-user",
            "smtp_password": SecretStr("private-test-password"),
            "mail_sender": "Enterprise PPM <accounts@example.com>",
        }
    )


def payload(kind):
    return {
        "kind": kind,
        "to": "recipient@example.com",
        "link": "https://ppm.example.com/account/complete#token=private-fixture-link",
        "expires_at": "2026-10-11T12:00:00+00:00",
        "organization_name": "Northstar Training",
        "role": "Project Manager",
    }


@pytest.mark.parametrize("kind", ["register", "invite", "activate", "reset"])
def test_messages_contain_correct_private_journey(settings, kind):
    message = account_message(smtp_settings(settings), payload(kind), uuid4())
    body = message.get_content()
    assert payload(kind)["link"] in body
    assert "2026-10-11T12:00:00+00:00" in body
    assert "used once" in body and "Do not forward" in body
    assert "https://ppm.example.com/login" in body
    assert "@example.com>" in message["Message-ID"] and message["Date"]
    assert "private-test-password" not in message.as_string()
    if kind == "invite":
        assert "Northstar Training" in message["Subject"]
        assert "Project Manager" in body and "existing password" in body
        assert "Admin" in body
    if kind == "register":
        assert "organization is created after verification" in body
        assert "https://ppm.example.com/signup" in body
    if kind == "reset":
        assert "signs out existing sessions" in body
        assert "https://ppm.example.com/account/reset" in body


def test_organization_linebreaks_cannot_inject_headers(settings):
    data = payload("invite") | {"organization_name": "Northstar\r\nBcc: stranger@example.com"}
    message = account_message(smtp_settings(settings), data, uuid4())
    assert message["Bcc"] is None


@pytest.mark.parametrize("refused", [False, True])
def test_smtp_tls_auth_and_recipient_acceptance(settings, monkeypatch, refused):
    calls = []

    class Server:
        def __init__(self, host, port, timeout):
            assert (host, port, timeout) == ("smtp.example.com", 587, 10)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def starttls(self, context):
            assert context.check_hostname
            calls.append("tls")

        def login(self, user, password):
            assert (user, password) == ("test-user", "private-test-password")
            calls.append("auth")

        def send_message(self, message):
            assert message["To"] == "recipient@example.com"
            calls.append("send")
            return {"recipient@example.com": (550, b"rejected")} if refused else {}

    monkeypatch.setattr("ppm_api.account_mail.smtplib.SMTP", Server)
    if refused:
        with pytest.raises(smtplib.SMTPRecipientsRefused):
            smtp_delivery(smtp_settings(settings), payload("invite"), uuid4())
    else:
        smtp_delivery(smtp_settings(settings), payload("invite"), uuid4())
    assert calls == ["tls", "auth", "send"]


@pytest.mark.parametrize(
    "change",
    [
        {"smtp_host": ""},
        {"smtp_host": "smtp.example.com invalid"},
        {"mail_sender": "invalid"},
        {"mail_sender": "accounts@example.com\r\nBcc: stranger@example.com"},
        {"smtp_user": ""},
        {"smtp_password": ""},
        {"smtp_port": 465},
    ],
)
def test_smtp_configuration_fails_before_accepting_requests(settings, change):
    data = smtp_settings(settings).model_dump() | change
    with pytest.raises(ValidationError) as error:
        Settings(**data)
    assert "private-test-password" not in str(error.value)


def test_mail_model_error_reports_names_without_secrets(settings, monkeypatch):
    monkeypatch.setenv("PPM_APP_ENV", "test")
    monkeypatch.setenv("PPM_DATABASE_URL", settings.database_url.get_secret_value())
    monkeypatch.setenv("PPM_REDIS_URL", settings.redis_url.get_secret_value())
    monkeypatch.setenv("PPM_JWT_SECRET", settings.jwt_secret.get_secret_value())
    monkeypatch.setenv("PPM_STORAGE_ROOT", str(settings.storage_root))
    monkeypatch.setenv("PPM_MAIL_MODE", "smtp")
    monkeypatch.setenv("PPM_SMTP_HOST", "")
    monkeypatch.setenv("PPM_SMTP_PASSWORD", "private-test-password")
    with pytest.raises(RuntimeError) as error:
        load_settings()
    assert "PPM_MAIL_CONFIGURATION" in str(error.value)
    assert "private-test-password" not in str(error.value)


def test_local_mode_and_smtp_relay_are_deliberate(settings):
    assert "no inbox email" in delivery_instructions(settings)
    assert "spam folder" in delivery_instructions(smtp_settings(settings))
    assert "30 minutes" in delivery_instructions(smtp_settings(settings), reset=True)
    data = smtp_settings(settings).model_dump() | {"smtp_user": "", "smtp_password": ""}
    assert Settings(**data).mail_mode == "smtp"
