function r(item, out){ out += `  <li id="${item.id}" class="${item.qty > 3 ? "big" : "small"}">${item.name}: ${item.qty}</li>\n`; return out; }
function c(s,i){ s += "x" + i; return s; }
