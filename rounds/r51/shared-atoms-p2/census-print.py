import sys
p=sys.argv[1]+'/core/src/runtime.rs'
s=open(p).read()
start=s.index('        // The shared-atoms probe: `QJS_ATOM_CENSUS` set prints each report\'s')
end=s.index('        let mut report = self.heap.report();')
s=s[:start]+s[end:]
a='''            code.source_bytes += unit.source.as_ref().map_or(0, |source| source.len());
        }
        report
    }'''
b='''            code.source_bytes += unit.source.as_ref().map_or(0, |source| source.len());
        }
        // The shared-atoms probe: `QJS_ATOM_CENSUS` set prints each report's
        // census and reserved bytes (`docs/shared-atoms.md`).
        if std::env::var_os("QJS_ATOM_CENSUS").is_some() {
            eprintln!(
                "atom census [{}] reserved={} live={}: {}",
                std::thread::current().name().unwrap_or("?"),
                report.reserved_bytes(),
                report.gc.live_bytes,
                self.atom_census()
            );
        }
        report
    }'''
assert a in s; s=s.replace(a,b,1)
open(p,'w').write(s)
