# ADR-0003: No ORDER BY RANDOM() on large tables

Status: accepted. Date: 2026-05-20.

## Context

`SELECT ... ORDER BY RANDOM() LIMIT 1` on `users` (1.2M rows) caused p99 latency of 900ms on the ops dashboard and a full-table scan per request.

## Decision

`ORDER BY RANDOM()` and `OFFSET floor(random() * count)` are banned on any table expected to exceed 10k rows. Random selection must use an index seek. Reference implementation: `UserRepository.get_random`.
