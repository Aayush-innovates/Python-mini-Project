from components.visualizations import format_minimized_equation, parse_sop_terms, _gate_body_svg

print(format_minimized_equation("B'*C + A'*C'"))
print(parse_sop_terms("B'*C + A'*C'"))
print(parse_sop_terms("(A & C) | (B & C)"))
print(format_minimized_equation("(A & C) | (B & ~C)"))
body, tip, cy = _gate_body_svg("NAND", 10, 10, 100, 80)
print("gate ok", tip)
