def react_polymer(polymer: str) -> tuple[str, int]:
    """
    Process polymer chain reaction and return stable polymer + reaction count.
    Uses a stack-based approach that handles all reactions in one pass.
    
    Args:
        polymer: Input polymer string
        
    Returns:
        tuple: (stable_polymer, reaction_count)
    """
    if not polymer:
        return "", 0
        
    stack = []
    reaction_count = 0
    
    for char in polymer:
        if stack and will_react(stack[-1], char):
            # Reaction occurs - remove the top of stack
            stack.pop()
            reaction_count += 1
        else:
            stack.append(char)
    
    return ''.join(stack), reaction_count

def will_react(a: str, b: str) -> bool:
    """
    Check if two monomers will react.
    They react if they are the same letter but different cases.
    """
    return a != b and a.lower() == b.lower()

def process_multiple_polymers(polymers: list) -> tuple[str, int]:
    """
    Process multiple polymers by concatenating and reacting.
    
    Args:
        polymers: List of polymer strings
        
    Returns:
        tuple: (final_polymer, total_reaction_count)
    """
    if not polymers:
        return "", 0
    
    # Concatenate all polymers
    combined = ''.join(polymers)
    
    # React the combined polymer
    result, reaction_count = react_polymer(combined)
    
    return result, reaction_count