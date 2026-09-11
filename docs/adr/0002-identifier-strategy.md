# ADR-0002: Identifier strategy

Status: accepted. Date: 2026-03-09.

## Context

We need primary keys that are safe to expose in URLs, generated app-side without a DB round trip, and cheap to insert at high volume.

## Decision

- UUIDv4 (`app.core.ids.new_principal_id`) for `users` and `api_keys`.
- UUIDv7 (`app.core.ids.new_record_id`) for `orders` and `order_events`, which are high volume and append-heavy. Keyset pagination on these tables uses the primary key directly.

## Consequences

- No sequences, no round trip on insert.
- Order ids can be used as pagination cursors.
