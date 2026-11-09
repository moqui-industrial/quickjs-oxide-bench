// HTML escape as Moqui's templates do it ($esc in template.rs): 100 strings,
// half with characters to escape.
const $esc = (v) => String(v).replace(/[&<>"']/g, (c) => c === "&" ? "&amp;" : c === "<" ? "&lt;" : c === ">" ? "&gt;" : c === '"' ? "&quot;" : "&#39;");
var strs = [];
for (var i = 0; i < 100; i++)
  strs.push(i % 2 ? 'Item <b>' + i + '</b> & "quoted" \'name\' ' + i : 'Plain item name number ' + i + ' with text');
var N = typeof scale === 'number' ? scale : 4000, total = 0;
for (var n = 0; n < N; n++)
  for (var j = 0; j < 100; j++) total += $esc(strs[j]).length;
print(total);
