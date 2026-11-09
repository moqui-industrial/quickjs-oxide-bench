let n = 0;
for (let r = 0; r < 3000; r++) { let s = ''; for (let i = 0; i < 1000; i++) s += 'x' + i; n += s.length; }
print(n);
