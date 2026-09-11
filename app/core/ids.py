"""Identifier generation. Which table uses which is decided in ADR-0002."""

from uuid import UUID, uuid4, uuid7

__all__ = ["new_principal_id", "new_record_id"]


def new_principal_id() -> UUID:
    return uuid4()


def new_record_id() -> UUID:
    return uuid7()
