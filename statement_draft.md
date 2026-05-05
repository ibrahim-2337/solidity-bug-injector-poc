# Humanized Short Statement (More "Research-Hacker" Vibe)

**Subject:** SANAD Summer RA – Solidity Bug Injection 2026

Hi Tamer,

I'm reaching out because I'm really interested in the Undergraduate RA position at SANAD Lab. I've been following some of the work in automated bug injection (like the SolidiFI paper), and I’m fascinated by the idea of using program transformation to build better security benchmarks.

My background is in computer security and HPC (I’ve spent a lot of time optimizing data pipelines at the Mubadala Center), and I’ve been diving deep into Solidity and Foundry lately.

To see if I could actually wrap my head around the lab's workflow, I spent this past weekend hacking together a prototype of an **AST-based mutation engine**. You can check out the repo here: [https://github.com/ibrahim-2337/solidity-bug-injector-poc](https://github.com/ibrahim-2337/solidity-bug-injector-poc)

**What I got working:**
*   A Python script that pulls the **AST JSON** from a Forge build.
*   A traversal logic that identifies specific security modifiers (like `onlyOwner`) and prunes them using the exact source coordinates from the compiler.
*   A closed-loop validation where a Foundry exploit test confirms the bug is concretely exploitable.

Getting the AST pruning to align with the source range was a bit of a hurdle, but it's much more robust than the regex approach I started with. I'd love to bring this kind of hands-on experimentation to the lab and help build out the more complex mutation operators you mentioned in the posting.

I’ve attached my resume and transcript. Looking forward to hearing from you!

Best,

Ibrahim
