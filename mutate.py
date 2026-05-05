import json
import subprocess
import os

import shutil

# quick helper for forge commands
def sh(cmd):
    # use shutil.which to find forge in the PATH if the hardcoded one isn't there
    forge_bin = os.path.expanduser("~/.foundry/bin/forge")
    if not os.path.exists(forge_bin):
        forge_bin = shutil.which("forge") or "forge"
    
    cmd[0] = forge_bin
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    target = "src/Vault.sol"
    # forge puts the ast in the build artifacts
    artifact = "out/Vault.sol/Vault.json"
    
    print("--- sanad-mutator-poc ---")
    
    # 1. compile to get the AST
    print("[*] compiling to get the ast...")
    sh(["forge", "build"])
    
    if not os.path.exists(artifact):
        print("!! artifact not found. forge build failed?")
        return

    with open(artifact, "r") as f:
        data = json.load(f)
    
    ast = data.get("ast")
    if not ast:
        print("!! no ast in the json. weird.")
        return

    # 2. find the 'onlyOwner' modifier on the withdraw function
    # doing this via source ranges is way more precise than regex
    print("[*] crawling the ast...")
    
    src_range = None
    
    def walk(node):
        nonlocal src_range
        # look for the withdraw function
        if node.get("nodeType") == "FunctionDefinition" and node.get("name") == "withdraw":
            mods = node.get("modifiers", [])
            for m in mods:
                # find the onlyOwner modifier
                if m.get("modifierName", {}).get("name") == "onlyOwner":
                    src_range = m.get("src")
                    return
        
        # recursive walk
        for k, v in node.items():
            if isinstance(v, dict): walk(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict): walk(item)

    walk(ast)

    if not src_range:
        print("!! couldn't find the modifier in the ast. maybe it's already gone?")
        return

    print(f"[*] found it. source range: {src_range}")

    # 3. Nuke the modifier using the range from the compiler
    # format is start:length:fileIndex
    start, length, _ = map(int, src_range.split(":"))
    
    with open(target, "r") as f:
        code = f.read()

    # replace with spaces to keep the file offsets mostly sane for the compiler
    mutated = code[:start] + (" " * length) + code[start + length:]
    
    with open(target, "w") as f:
        f.write(mutated)
    
    print("[+] mutation done. contract is now vulnerable.")

    # 4. verify the exploit
    print("[*] running foundry test to prove the exploit works...")
    res = sh([forge_bin, "test"])
    
    # print(res.stdout) # debug

    if "[PASS]" in res.stdout:
        print("\n[SUCCESS] Exploit worked. Bug injection verified via AST.")
        exit(0)
    else:
        print("\n[!] something went wrong. test didn't pass.")
        print(res.stdout)
        print(res.stderr)
        exit(1)

if __name__ == "__main__":
    main()
