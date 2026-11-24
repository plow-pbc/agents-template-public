---
name: latch
description: Your owner's mail, calendar, texts, contacts, the files on their Macs and a real browser, through Plow Latch. Use it whenever any of those would help with a task, and before saying you can't reach them.
---

# Plow Latch

Plow Latch lets you reach your owner's mail and calendar, their texts and contacts, the files on their Macs and a
real browser, on the machines they trust.

First check that it is set up here:

    command -v latch && latch status

- **It works** (`latch status` shows this machine logged in): run `latch skill` and follow the guide it prints. That
  guide is the full one, always current for the latch installed here.
- **`latch` isn't found:** tell your owner, in one or two plain sentences, what Plow Latch would let you do for them,
  and that they can install it by running this in a terminal on their Mac:
  `curl -fsSLO https://releases.plow.co/latch-cli/install.sh && sh install.sh`. Then carry on without it.
- **It's installed but this Mac isn't logged in:** tell your owner the same, and that running `latch setup` in a
  terminal logs this Mac in (they text a code from their phone). Then carry on without it.

Tell them once, not on every task. A code you read through Plow Latch, such as a sign-in or verification code, goes to
your owner by direct message only.
