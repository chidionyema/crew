# The transcript corpus

The estate's own behaviour is recorded in `~/.claude/projects` as one jsonl file
per session. Goals 2 and 3 in `PLAN.md` both depend on it. It was being deleted.

## What was happening

Measured 2026-08-23:

    oldest surviving file   exactly 30.00 days old
    .last-cleanup           stamped 16:04 the same day
    file count              81,378 at 15:10, 81,090 at 16:10
    cleanupPeriodDays       not set in any settings file

288 files went in an hour. The default retention was doing it, and no setting
anywhere said so out loud.

## What was done

    ~/.claude/archive/transcripts-20260823.tar.zst
    984 MB, holding 6,298,808,320 bytes, 6.4x

Verified two ways. `zstd -t` passes on the whole file. The archive holds 81,091
`.jsonl` members against 81,091 on live disk, an exact match.

`cleanupPeriodDays` is now set to 30 deliberately, rather than left unset. The
live tree stays at its steady 6.4 GB and the archive carries everything older.
A longer live window was considered and rejected: the disk is at 98 percent with
9 GB free, and 60 days would need 13 GB.

## Restoring

    zstd -dc ~/.claude/archive/transcripts-20260823.tar.zst | tar -xf - -C <dest>

A tarball moves to any machine without asking a vendor for it, which is what
LAW 19 requires of an institutional memory.

## Not done yet

The capture is a one-off. Nothing repeats it, so the window between today and
the next capture is unprotected. Making it a scheduled job is the next step on
goal 3, and under LAW 32 that job ships with a demo and an onboarding page
before it is pushed.

The disk sitting at 98 percent is a separate problem and belongs to operations.
Flagging it, not fixing it.
