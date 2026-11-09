// Template literals: a list of 100 items rendered as a template would.
var items = [];
for (var i = 0; i < 100; i++) items.push({ name: 'Item ' + i, qty: i % 7, id: 'I' + i });
function render(title) {
  var out = `<h1>${title}</h1>\n<ul>\n`;
  for (var k = 0; k < items.length; k++) {
    var item = items[k];
    out += `  <li id="${item.id}" class="${item.qty > 3 ? 'big' : 'small'}">${item.name}: ${item.qty}</li>\n`;
  }
  return out + `</ul>\n`;
}
var N = typeof scale === 'number' ? scale : 8000, total = 0;
for (var n = 0; n < N; n++) total += render('List ' + n).length;
print(total);
