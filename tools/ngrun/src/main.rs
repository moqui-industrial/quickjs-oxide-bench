//! Runs a script file on quickjs-ng (rquickjs 0.14, as Moqui embeds it) and
//! prints its completion value. `print` writes its argument.
use rquickjs::{Context, Function, Runtime, Value};

fn main() {
    let path = std::env::args().nth(1).expect("a script");
    let source = std::fs::read_to_string(&path).expect("readable");
    let runtime = Runtime::new().unwrap();
    let context = Context::full(&runtime).unwrap();
    context.with(|ctx| {
        let print = Function::new(ctx.clone(), |v: Value| {
            println!("{}", v.as_number().map(|n| n.to_string()).or_else(|| v.as_string().and_then(|s| s.to_string().ok())).unwrap_or_default());
        })
        .unwrap();
        ctx.globals().set("print", print).unwrap();
        let result: Result<Value, _> = ctx.eval(source);
        if let Err(e) = result {
            let ex = ctx.catch();
            panic!("{e}: {ex:?}");
        }
    });
}
