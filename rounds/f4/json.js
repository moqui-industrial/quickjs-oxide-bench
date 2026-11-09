// js_speed's "JSON stringify + parse of 100 objects".
function f() {
  var l = [];
  for (var i = 0; i < 100; i++) l.push({ id: 'I' + i, qty: i, name: 'Item ' + i });
  return JSON.parse(JSON.stringify(l)).length;
}
var N = typeof scale === 'number' ? scale : 20000, total = 0;
for (var n = 0; n < N; n++) total += f();
print(total);
