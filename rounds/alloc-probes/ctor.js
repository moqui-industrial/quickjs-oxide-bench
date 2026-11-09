// A constructor adding 20 properties to each of 5,000 instances, plain
// assignment and a computed-key [[Set]] miss.
function P(i) {
  this.a0 = i; this.a1 = i; this.a2 = i; this.a3 = i; this.a4 = i; this.a5 = i; this.a6 = i;
  this.a7 = i; this.a8 = i; this.a9 = i; this.b0 = i; this.b1 = i; this.b2 = i; this.b3 = i;
  this.b4 = i; this.b5 = i; this.b6 = i; this.b7 = i; this.b8 = i; this.b9 = i;
}
function Q(i) { for (var k = 0; k < 20; k++) this['k' + k] = i; }
var keep = [];
for (var i = 0; i < 5000; i++) { keep.push(new P(i)); keep.push(new Q(i)); }
print(keep.length);
