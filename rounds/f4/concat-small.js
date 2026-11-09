// js_speed's "1000 string concatenations".
var N = typeof scale === 'number' ? scale : 300, total = 0;
function f() { var s = ''; for (var i = 0; i < 1000; i++) s += 'x' + i; return s.length; }
for (var n = 0; n < N; n++) total += f();
print(total);
