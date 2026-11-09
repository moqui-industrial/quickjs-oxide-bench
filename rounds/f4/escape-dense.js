// $esc over markup-dense strings: most characters escaped.
const $esc = (v) => String(v).replace(/[&<>"']/g, (c) => c === "&" ? "&amp;" : c === "<" ? "&lt;" : c === ">" ? "&gt;" : c === '"' ? "&quot;" : "&#39;");
var strs = [];
for (var i = 0; i < 100; i++) strs.push('<a href="/x?a=' + i + '&b=2">\'' + i + '\'</a><br/>');
var N = typeof scale === 'number' ? scale : 1500, total = 0;
for (var n = 0; n < N; n++)
  for (var j = 0; j < 100; j++) total += $esc(strs[j]).length;
print(total);
