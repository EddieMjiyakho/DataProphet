#!/usr/bin/env python3
"""
Debug script to understand polymer reaction behavior
"""
def react_polymer_debug(polymer: str) -> tuple[str, int]:
    """
    Process polymer chain reaction with debug output
    """
    print(f"Input: {polymer}")
    
    stack = []
    reaction_count = 0
    
    for i, char in enumerate(polymer):
        print(f"Step {i}: char='{char}', stack={stack}")
        
        if stack and will_react(stack[-1], char):
            # Reaction occurs
            reacted_with = stack.pop()
            reaction_count += 1
            print(f"  REACTION: '{reacted_with}' + '{char}' -> removed")
        else:
            stack.append(char)
            print(f"  ADDED: '{char}'")
    
    result = ''.join(stack)
    print(f"Final: '{result}', reactions: {reaction_count}")
    print("---")
    return result, reaction_count

def will_react(a: str, b: str) -> bool:
    return a != b and a.lower() == b.lower()

# Test the assignment example
print("Testing: AaefxxxXB")
react_polymer_debug("AaefxxxXB")

print("\nTesting step by step as described in assignment:")
print("1. Aa reacts -> efaaaAB becomes efaaaAB (A and a removed)")
print("2. xx reacts -> efxxB becomes efxxB (x and x don't react - they're same case)")
print("3. XB doesn't react -> final: efxxB")

print("\nWait, let me check the assignment again...")
print("Assignment says: AaefxxxXB should become efB")
print("This suggests:")
print("- Aa reacts (remove A and a)")
print("- Then xx should react (but x and x are same case, so they shouldn't)")
print("- Something else must be happening...")

print("\nLet me test individual pairs:")
print(f"a and A: {will_react('a', 'A')}")  # Should be True
print(f"x and x: {will_react('x', 'x')}")  # Should be False (same case)
print(f"x and X: {will_react('x', 'X')}")  # Should be True
print(f"X and B: {will_react('X', 'B')}")  # Should be False

print("\nLet me trace through 'AaefxxxXB':")
print("A + a -> react (remove both)")
print("e -> add")
print("f -> add") 
print("x -> add")
print("x -> same case, no reaction, add")
print("x -> same case, no reaction, add")
print("X -> different case from previous x, should react!")
print("B -> add")
print("So we should get: efxxB but assignment says efB")
print("This suggests the assignment example might have a typo, or we're missing something.")

print("\nLet me check if there are consecutive reactions:")
test_string = "AaefxxxXB"
print(f"Original: {test_string}")

# Maybe the reaction continues after the first pass?
def react_until_stable(polymer: str):
    current = polymer
    total_reactions = 0
    pass_num = 1
    
    while True:
        print(f"Pass {pass_num}: {current}")
        result, reactions = react_polymer_debug(current)
        if result == current:  # No change
            break
        current = result
        total_reactions += reactions
        pass_num += 1
    
    return current, total_reactions

print("\nTesting with multiple passes:")
final, total_reacts = react_until_stable("AaefxxxXB")
print(f"Final after all passes: {final}, total reactions: {total_reacts}")