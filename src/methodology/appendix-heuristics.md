# Appendix: Tool Heuristics (Agent-Maintained)

This appendix is a living document. When an agent encounters a non-obvious
Gaudi/k4FWCore/EDM4hep pattern, it records the working solution here so
subsequent sessions start with working knowledge rather than rediscovering
the same pitfalls.

**Maintenance rules:**
- Check this appendix before querying external docs for a listed tool.
- If an entry exists and is sufficient, use it without re-querying.
- If an entry is missing or incomplete, query current docs, use the result,
  and add a note to `experiment_log.md` flagging the gap (update the
  appendix after the phase completes).
- Keep entries concise — heuristics and gotchas, not full API references.

---

## k4FWCore Functional Patterns

*(Entries added as agents encounter patterns)*

**Common pitfall:** Functional algorithm template parameters must match the
`operator()` signature exactly. A `Producer<edm4hep::MCParticleCollection()>`
must have `operator()() const` returning `edm4hep::MCParticleCollection` by
value — returning a pointer or reference will not compile.

**Constructor key syntax:** The `KeyValues` constructor argument sets both
the default collection name and the property name used in the steering file.
```cpp
// Sets default to "MCParticles"; overridable via MyProducer.MCParticles = "..."
: k4FWCore::Producer(name, svcLoc, KeyValues("MCParticles", "MCParticles"))
```

---

## EDM4hep

*(Entries added as agents encounter patterns)*

**MCParticle creation:**
```cpp
auto particles = edm4hep::MCParticleCollection();
auto p = particles.create();
p.setMass(0.139f);   // GeV
p.setPDG(211);       // pi+
// momentum is a Vector3f: {px, py, pz}
p.setMomentum({0.f, 0.f, 1.f});
```

**Reading a collection in Consumer:**
```cpp
for (const auto& p : particles) {
  float e = p.getEnergy();
  auto mom = p.getMomentum();  // edm4hep::Vector3f
  float pt = std::sqrt(mom.x*mom.x + mom.y*mom.y);
}
```

---

## CMake / Gaudi Build

*(Entries added as agents encounter patterns)*

**Missing `GaudiPluginService` linker error:** Add `Gaudi::GaudiPluginService`
to `LINK_LIBRARIES`. This provides the plugin registration infrastructure
that `DECLARE_COMPONENT` depends on. Required whenever `DECLARE_COMPONENT`
is used.

**`gaudi_add_module` vs `gaudi_add_library`:** Use `gaudi_add_module` for
algorithm plugins (loaded at runtime). Use `gaudi_add_library` only for
shared utility libraries that other targets link against.

---

## ROOT / ITHistSvc

*(Entries added as agents encounter patterns)*

**Histogram registration path:** Must start with `/` and match the
`THistSvc.Output` stream name. For `Output = ["out DATAFILE='x.root' ..."]`,
register histograms under `/out/`:
```cpp
m_histSvc->regHist("/out/energy", m_hEnergy);
```
Mismatched paths produce a silent registration failure — the histogram
exists in memory but is not written to file.
