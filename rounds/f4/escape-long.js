// $esc over longer text: 100 paragraphs of 200-400 characters, a few specials each.
const $esc = (v) => String(v).replace(/[&<>"']/g, (c) => c === "&" ? "&amp;" : c === "<" ? "&lt;" : c === ">" ? "&gt;" : c === '"' ? "&quot;" : "&#39;");
var strs = [];
for (var i = 0; i < 100; i++) {
  var p = '';
  for (var k = 0; k < 6 + i % 5; k++) p += 'Lorem ipsum dolor sit amet, item ' + (i * k) + ' consectetur ';
  strs.push(i % 3 ? p + ' & <tag> "q"' : p);
}
var N = typeof scale === 'number' ? scale : 600, total = 0;
for (var n = 0; n < N; n++)
  for (var j = 0; j < 100; j++) total += $esc(strs[j]).length;
print(total);
