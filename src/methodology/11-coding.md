## 11. Coding Practices

### 11.1 Git

**Conventional commits:** `<type>(phase): <description>`.
Types: `feat`, `fix`, `build`, `test`, `docs`, `refactor`, `chore`.

Examples:
```
feat(phase2): implement MCParticle energy filter transformer
fix(phase3): add ROOT::Hist to LINK_LIBRARIES
docs(phase5): add doxygen comments to MyAlg header
```

**Commit after every phase.** Commits are checkpoints — if an agent session
crashes, resume from the last commit.

### 11.2 C++ Code Quality

**Gaudi idioms (mandatory):**
- Use `Gaudi::Property<T>` for all configurable parameters
- Use `info()` / `debug()` / `warning()` / `error()` — never `std::cout`
- Use PODIO/EDM4hep collection APIs — never raw `new`/`delete` for event data
- Override methods must have `override` keyword
- Destructors should be `= default` unless non-trivial cleanup is needed

**Modern C++ practices:**
- Use `const auto&` for loop variables over collections
- Use `auto` for iterator types
- Prefer range-based `for` loops over index loops
- Use `nullptr` not `NULL` or `0` for pointers

**What not to do:**
```cpp
// BAD: std::cout
std::cout << "Processing event" << std::endl;

// GOOD: Gaudi logging
info() << "Processing event " << eventNumber << endmsg;

// BAD: raw memory
MCParticleCollection* output = new MCParticleCollection();

// GOOD: PODIO API
auto output = edm4hep::MCParticleCollection();
```

### 11.3 CMake Quality

- Always use `gaudi_add_module` for algorithm plugins (not `add_library`)
- List all required packages in `LINK_LIBRARIES` — missing entries cause
  linker errors at build time, not compile time
- Use `file(GLOB _sources src/components/*.cpp)` to pick up all components
- Install both the library target and the `options/` directory

### 11.4 Python Steering Files

- Use keyword arguments for `ApplicationMgr` — easier to read and maintain
- Configure `THistSvc.Output` when booking histograms:
  ```python
  histsvc = THistSvc()
  histsvc.Output = ["output DATAFILE='output.root' OPT='RECREATE'"]
  ```
- Set `OutputLevel` explicitly (INFO for normal use, DEBUG for development)
- Name algorithm instances meaningfully:
  ```python
  alg = MyProducer("MyProducer")  # not MyProducer("a1")
  ```

### 11.5 Logging in Phase 4 Python Scripts

No bare `print()` in validation scripts:

```python
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

log.info("Found %d entries in histogram", n)
```
