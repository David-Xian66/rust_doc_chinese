import re

en = 'A B'
escaped = re.escape(en)
print('escaped repr:', repr(escaped), 'len:', len(escaped))
# Should be 'A\\ B' (4 chars: A, \, space, B)
# Wait re.escape('A B') gives 'A\\ B' which is 4 chars: A, \, space, B? No that's 4 chars: A, \, space... but B is missing.
# Actually re.escape('A B') = 'A\\ B' in Python string literal which is 4 chars: A, \, space... no, A (1) + \ (1) + space (1) + B (1) = 4 chars. Let me verify.

print('chars:', list(escaped))