# Gaudi Algorithm Conventions

Reference for generating correct, idiomatic Gaudi/k4FWCore algorithms.

---

## 1. Pattern Selection

### Use `k4FWCore::Producer` when:
- The algorithm **creates** a new collection from scratch (no event input collections).
- Example: generating MC particles, creating dummy data, reading an external file.

```cpp
#include "k4FWCore/Producer.h"
#include "edm4hep/MCParticleCollection.h"

struct MyProducer final : k4FWCore::Producer<edm4hep::MCParticleCollection()> {
  MyProducer(const std::string& name, ISvcLocator* svcLoc);
  edm4hep::MCParticleCollection operator()() const override;
  Gaudi::Property<float> m_energy{this, "Energy", 10.0f, "Beam energy in GeV"};
};
DECLARE_COMPONENT(MyProducer)
```

### Use `k4FWCore::Consumer` when:
- The algorithm **reads** collections and produces no new event-level output
  (e.g., fills histograms, writes text, validates, counts).

```cpp
#include "k4FWCore/Consumer.h"
#include "edm4hep/MCParticleCollection.h"

struct MyConsumer final : k4FWCore::Consumer<void(const edm4hep::MCParticleCollection&)> {
  MyConsumer(const std::string& name, ISvcLocator* svcLoc);
  void operator()(const edm4hep::MCParticleCollection& particles) const override;
};
DECLARE_COMPONENT(MyConsumer)
```

### Use `k4FWCore::Transformer` when:
- The algorithm **reads** one or more collections and **produces exactly one**
  new collection.
- Example: filtering particles, computing derived quantities, applying corrections.

```cpp
#include "k4FWCore/Transformer.h"
#include "edm4hep/MCParticleCollection.h"
#include "edm4hep/RecoParticleCollection.h"

struct MyTransformer final
    : k4FWCore::Transformer<edm4hep::RecoParticleCollection(
          const edm4hep::MCParticleCollection&)> {
  MyTransformer(const std::string& name, ISvcLocator* svcLoc);
  edm4hep::RecoParticleCollection operator()(
      const edm4hep::MCParticleCollection& input) const override;
};
DECLARE_COMPONENT(MyTransformer)
```

### Use `k4FWCore::MultiTransformer` when:
- The algorithm **reads** one or more collections and **produces two or more**
  new collections simultaneously.
- Example: digitisation producing a hit collection and a hit-to-sim-hit link
  collection (see DDCaloDigi in k4GaudiPandora).

```cpp
#include <k4FWCore/Transformer.h>
#include <edm4hep/CalorimeterHitCollection.h>
#include <edm4hep/CaloHitSimCaloHitLinkCollection.h>
#include <edm4hep/SimCalorimeterHitCollection.h>
#include <edm4hep/EventHeaderCollection.h>

using retType = std::tuple<edm4hep::CalorimeterHitCollection,
                           edm4hep::CaloHitSimCaloHitLinkCollection>;

struct MyMultiTransformer final
    : k4FWCore::MultiTransformer<retType(
          const edm4hep::SimCalorimeterHitCollection&,
          const edm4hep::EventHeaderCollection&)> {

  MyMultiTransformer(const std::string& name, ISvcLocator* svcLoc)
      : MultiTransformer(name, svcLoc,
                         {
                             KeyValues("InputHits",   {"SimCalorimeterHits"}),
                             KeyValues("HeaderName",  {"EventHeader"}),
                         },
                         {
                             KeyValues("OutputHits",  {"CalorimeterHits"}),
                             KeyValues("OutputLinks",  {"CaloHitLinks"}),
                         }) {}

  StatusCode initialize() override;

  retType operator()(const edm4hep::SimCalorimeterHitCollection& simHits,
                     const edm4hep::EventHeaderCollection& headers) const override;
};
DECLARE_COMPONENT(MyMultiTransformer)
```

Key points:
- The constructor passes `KeyValues` pairs to the base class for every input
  and output. The first argument is the property name exposed to the steering
  file; the second is the default collection name.
- `operator()` is `const` — use `mutable` for any state that must be mutated
  (e.g., histograms, counters).
- There is **no** `execute()` method; the framework calls `operator()`.

---

## 2. Property Declarations

Always use `Gaudi::Property<T>` — never bare member variables for
user-configurable parameters.

```cpp
// Scalar types
Gaudi::Property<float>       m_minPt{this, "MinPt", 0.5f,  "Min pT cut [GeV]"};
Gaudi::Property<int>         m_maxN {this, "MaxN",  100,   "Max number of particles"};
Gaudi::Property<std::string> m_coll {this, "CollectionName", "MCParticles", "Input collection"};

// Vector types
Gaudi::Property<std::vector<float>> m_cuts{this, "Cuts", {0.5f, 1.0f}, "Cut values"};
```

---

## 3. Logging

Use Gaudi message streams — never `std::cout` or `printf`.

```cpp
info()    << "Processing event with " << nParticles << " particles" << endmsg;
debug()   << "Particle pT = " << pt << " GeV" << endmsg;
warning() << "Empty input collection" << endmsg;
error()   << "Failed to retrieve service" << endmsg;
```

---

## 4. Histogramming with `Gaudi::Accumulators`

The modern approach for histogramming in k4FWCore functional algorithms
(Transformer, MultiTransformer, Producer, Consumer) is
`Gaudi::Accumulators::StaticHistogram` / `StaticWeightedHistogram`.
This avoids `ITHistSvc` boilerplate entirely — histograms self-register with
the owning algorithm via the `this` pointer at construction time.

This pattern is used by DDCaloDigi in k4GaudiPandora.

### Include

```cpp
#include <Gaudi/Accumulators/RootHistogram.h>
```

### Declaration (in class body)

Because `operator()` is `const`, histogram members must be `mutable`.

```cpp
// 1D unweighted histogram: ++h[x]
mutable Gaudi::Accumulators::StaticHistogram<1> m_hNHits{
    this, "nHits", "Number of hits per event", {100, 0., 1000.}};

// 1D weighted histogram: h[x] += weight
mutable Gaudi::Accumulators::StaticWeightedHistogram<1> m_hEnergy{
    this, "energy", "Hit energy profile", {200, 0., 100.}};

// 2D unweighted histogram: ++h[{x, y}]
mutable Gaudi::Accumulators::StaticHistogram<2> m_hXY{
    this, "hitXY", "Hit map XY", {{300, -4500., 4500.}, {300, -4500., 4500.}}};
```

Constructor arguments: `{this, "name", "title", {nBins, min, max}}` for 1D,
`{{nBinsX,xMin,xMax}, {nBinsY,yMin,yMax}}` for 2D.

### No booking step needed

There is no `regHist()` or `book()` call. The histograms are ready to use
as soon as the algorithm object is constructed.

### Filling (inside `operator()`)

```cpp
// Unweighted 1D fill
++m_hNHits[static_cast<double>(simHits.size())];

// Weighted 1D fill
m_hEnergy[hit.getEnergy()] += calibrationWeight;

// Unweighted 2D fill
++m_hXY[{hit.getPosition().x, hit.getPosition().y}];
```

### Full minimal example

```cpp
#include <Gaudi/Accumulators/RootHistogram.h>
#include <k4FWCore/Transformer.h>
#include <edm4hep/CalorimeterHitCollection.h>
#include <edm4hep/SimCalorimeterHitCollection.h>

struct CaloDigitizer final
    : k4FWCore::Transformer<edm4hep::CalorimeterHitCollection(
          const edm4hep::SimCalorimeterHitCollection&)> {

  CaloDigitizer(const std::string& name, ISvcLocator* svcLoc)
      : Transformer(name, svcLoc,
                    KeyValues("InputHits", {"SimCalorimeterHits"}),
                    KeyValues("OutputHits", {"CalorimeterHits"})) {}

  edm4hep::CalorimeterHitCollection operator()(
      const edm4hep::SimCalorimeterHitCollection& simHits) const override {

    edm4hep::CalorimeterHitCollection output;
    for (const auto& sh : simHits) {
      ++m_hNHits[1.0];                    // count hits
      m_hEnergy[sh.getEnergy()] += 1.0;  // energy spectrum
      auto hit = output.create();
      hit.setEnergy(sh.getEnergy() * m_calibCoeff);
    }
    return output;
  }

  Gaudi::Property<float> m_calibCoeff{this, "CalibCoeff", 1.0f, "Calibration coefficient"};

  mutable Gaudi::Accumulators::StaticHistogram<1> m_hNHits{
      this, "nHits", "Hits per event", {200, 0., 200.}};
  mutable Gaudi::Accumulators::StaticWeightedHistogram<1> m_hEnergy{
      this, "energy", "Hit energy [GeV]", {200, 0., 10.}};
};
DECLARE_COMPONENT(CaloDigitizer)
```

### Steering file for histogram output

```python
from Configurables import Gaudi__Histograming__Sink__Root as RootHistoSink
histSink = RootHistoSink("RootHistoSink")
histSink.FileName = "histograms.root"

from Gaudi.Configuration import ApplicationMgr
ApplicationMgr(ExtSvc=[histSink], ...)
```

---

## 5. CMakeLists.txt Pattern

```cmake
file(GLOB _sources src/components/*.cpp)

gaudi_add_module(MyAlgorithmPlugins
  SOURCES ${_sources}
  LINK_LIBRARIES
    Gaudi::GaudiKernel
    k4FWCore::k4FWCore
    EDM4HEP::edm4hep
    ROOT::Hist      # if using ROOT histograms
)

install(TARGETS MyAlgorithmPlugins
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

install(DIRECTORY options DESTINATION ${CMAKE_INSTALL_DATADIR}/MyAlgorithm)
```

---

## 6. Python Steering File

### Minimal (no I/O):
```python
from Gaudi.Configuration import ApplicationMgr, INFO
from Configurables import MyAlg

alg = MyAlg("MyAlg")
alg.MinPt = 1.0

ApplicationMgr(
    TopAlg=[alg],
    EvtSel="NONE",
    EvtMax=100,
    OutputLevel=INFO,
)
```

### With file I/O (k4FWCore functional):
```python
from Gaudi.Configuration import ApplicationMgr, INFO
from Configurables import IOSvc, MyProducer

ioDefs = IOSvc()
ioDefs.Output = "output.root"

producer = MyProducer("MyProducer")
producer.Energy = 91.2

ApplicationMgr(
    TopAlg=[producer],
    EvtSel="NONE",
    EvtMax=100,
    ExtSvc=[ioDefs],
    OutputLevel=INFO,
)
```

### Running:
```bash
k4run options/myAlg.py
# or:
gaudirun.py options/myAlg.py
```

---

## 7. Common EDM4hep Types

| Type | Header | Use case |
|------|--------|---------|
| `edm4hep::MCParticleCollection` | `edm4hep/MCParticleCollection.h` | Generator-level particles |
| `edm4hep::ReconstructedParticleCollection` | `edm4hep/ReconstructedParticleCollection.h` | Reco-level particles |
| `edm4hep::TrackCollection` | `edm4hep/TrackCollection.h` | Reconstructed tracks |
| `edm4hep::CalorimeterHitCollection` | `edm4hep/CalorimeterHitCollection.h` | Calorimeter hits |
| `edm4hep::SimTrackerHitCollection` | `edm4hep/SimTrackerHitCollection.h` | Simulated tracker hits |
| `edm4hep::ClusterCollection` | `edm4hep/ClusterCollection.h` | Calorimeter clusters |

Key accessors (MCParticle example):
```cpp
for (const auto& p : *collection) {
  p.getPDG();           // PDG ID (int)
  p.getEnergy();        // Energy in GeV
  p.getMomentum();      // edm4hep::Vector3f {px, py, pz}
  p.getMass();          // Mass in GeV
  p.getCharge();        // Charge
}
```

---

## 8. Project Directory Structure

Following k4-project-template:
```
MyAlgorithm/
├── CMakeLists.txt          (root — find_package + add_subdirectory)
├── README.md
├── MyAlgorithm/
│   ├── CMakeLists.txt      (gaudi_add_module)
│   ├── src/
│   │   └── components/
│   │       ├── MyAlg.h
│   │       └── MyAlg.cpp
│   └── options/
│       └── myAlg.py
└── test/
    └── CMakeLists.txt
```
