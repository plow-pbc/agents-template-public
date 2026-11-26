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
  and ask: "Would you like me to install it for you?" Then carry on without it.
  - **They say yes:** that yes, from your owner's own id, is their approval to install on their Mac; never install
    without it. Run `curl -fsSLO https://releases.plow.co/latch-cli/install.sh && sh install.sh` yourself. Then start
    `latch setup`: `latch setup --status` lists each step and the command that does it. Run the steps yourself. To
    sign in, run `latch login --events`, which needs no terminal. Its `code` line gives the `code`, the number to text
    it to (`send_to_display`) and an `sms_link` that opens Messages with both filled in. Texting that code is your
    owner's one step: tell them once, complete, where they are talking to you.
    - **In your DM with them:** "Last step, on your phone: text <code> to <send_to_display>. Or tap this, which opens
      Messages with it filled in: <sms_link>"
    - **In a group room:** the code never goes there. Send the DM message above first. Then say in the room: "Last
      step, on your phone: text the code I just sent you in a direct message (<where>) to <send_to_display>." For
      <where>, give the `link` your send's result gave for that DM; with none, "Plow → Direct messages → <your
      name>". Never write a mention or a name as a link.
    - **Then:** when its `verified` line comes, or `latch status` shows this Mac logged in, tell them Latch works.
  - **They say no:** drop it.
- **It's installed but this Mac isn't logged in:** tell your owner the same, and that running `latch setup` in a
  terminal logs this Mac in (they text a code from their phone). Then carry on without it.

Tell them once, not on every task. A code you read through Plow Latch, such as a sign-in or verification code, goes to
your owner by direct message only.
