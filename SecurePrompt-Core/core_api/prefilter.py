import math
import collections
import re

# Regex patterns derived from training phase
SYS_LEAK = re.compile(
    r"(system\s+prompt|you\s+are\s+now|always\s+say|<\|im_start\|>|<\|endoftext\|>)", 
    re.IGNORECASE
)
BASE64_OBFUSCATION = re.compile(r"(?:[A-Za-z0-9+/]{4}){10,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?")

def check_structural_prefilter(prompt: str) -> bool:
    """
    L4 Structural Check: Detects high entropy and excessive symbols.
    """
    if not prompt:
        return False
    
    # 1. Check special character ratio
    special_chars = sum(1 for c in prompt if not c.isalnum() and not c.isspace())
    if len(prompt) > 10 and special_chars / len(prompt) > 0.4:
        return True
        
    # 2. Shannon Entropy check (Find nonsense/garbled text)
    counter = collections.Counter(prompt)
    prob = [count / len(prompt) for count in counter.values()]
    entropy = -sum(p * math.log2(p) for p in prob)
    
    if entropy > 5.5: 
        return True
        
    return False

def check_regex_prefilter(prompt: str) -> bool:
    """
    Checks prompt against known fast-path regex patterns.
    Returns True if malicious, False otherwise.
    """
    if not isinstance(prompt, str):
        return False
    if SYS_LEAK.search(prompt):
        return True
    if BASE64_OBFUSCATION.search(prompt):
        return True
    return False