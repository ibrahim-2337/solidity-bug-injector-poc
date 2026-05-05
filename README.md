# sanad-mutator-poc

Quick proof-of-concept for automated Solidity bug injection using AST manipulation. Built this to experiment with the workflow SANAD Lab is working on.

## What is this?

The idea was to see if I could build a simple pipeline that:
1.  Takes a secure contract.
2.  Parses it into an **AST** to find specific security patterns (not just regex, which is too brittle).
3.  Injects a bug by pruning the AST nodes (specifically stripping an `onlyOwner` check).
4.  Validates that the bug is actually "real" by running a Foundry exploit test.

## How it works

*   **`src/Vault.sol`**: A simple vault that *should* be secure.
*   **`test/Exploit.t.sol`**: A Foundry test that tries to steal funds. In the baseline, it fails.
*   **`mutate.py`**: The "engine." It tells Forge to output the AST, walks the tree to find the `withdraw` function's modifier, and nuke it based on the exact source coordinates from the compiler.

## To run it

I'm using **Foundry** for the test suite and **Python** for the mutation script.

1.  **Check the baseline** (it should fail):
    `forge test`
2.  **Run the mutator**:
    `python3 mutate.py`

If it works, the script will show it found the modifier via the AST and that the Foundry test now passes.

## Why AST?
I initially tried doing this with regex, but it breaks if the code style changes. Using the AST coordinates from the compiler is way more robust and feels like the "right" way to do program analysis.
