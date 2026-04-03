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
- The algorithm **reads** one or more collections and **produces** one or more
  new collections.
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

### Use `Gaudi::Algorithm` when:
- The algorithm needs **persistent state across events** (e.g., accumulating
  histograms using `ITHistSvc`, running counters, multi-event accumulators).
- The algorithm needs **complex service access** in `initialize()`.
- The algorithm has a non-trivial `finalize()` step (writing files, computing
  final normalization).

```cpp
#include "Gaudi/Algorithm.h"
#include "GaudiKernel/ITHistSvc.h"

class MyAlg : public Gaudi::Algorithm {
public:
  MyAlg(const std::string& name, ISvcLocator* svcLoc);
  StatusCode initialize() override;
  StatusCode execute() override;
  StatusCode finalize() override;
private:
  Gaudi::Property<std::string> m_inputCollection{
      this, "InputCollection", "MCParticles", "Input collection name"};
  SmartIF<ITHistSvc> m_histSvc;
  TH1F* m_hEnergy = nullptr;
};
DECLARE_COMPONENT(MyAlg)
```

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

## 3. Data Handles (traditional Gaudi::Algorithm only)

For traditional algorithms, use `DataHandle<T>` for explicit data access:

```cpp
#include "k4FWCore/DataHandle.h"
#include "edm4hep/MCParticleCollection.h"

// In class declaration:
DataHandle<edm4hep::MCParticleCollection> m_inputHandle{
    "MCParticles", Gaudi::DataHandle::Reader, this};
DataHandle<edm4hep::MCParticleCollection> m_outputHandle{
    "FilteredParticles", Gaudi::DataHandle::Writer, this};

// In execute():
const auto* input = m_inputHandle.get();
auto* output = m_outputHandle.createAndPut();
```

---

## 4. Logging

Use Gaudi message streams — never `std::cout` or `printf`.

```cpp
info()    << "Processing event with " << nParticles << " particles" << endmsg;
debug()   << "Particle pT = " << pt << " GeV" << endmsg;
warning() << "Empty input collection" << endmsg;
error()   << "Failed to retrieve service" << endmsg;
```

---

## 5. Histogram Service (Gaudi::Algorithm)

For algorithms that book histograms:

```cpp
// In initialize():
m_histSvc = service<ITHistSvc>("THistSvc");
if (!m_histSvc) return StatusCode::FAILURE;

m_hEnergy = new TH1F("energy", "Particle energy;E [GeV];Entries", 100, 0, 100);
if (m_histSvc->regHist("/output/energy", m_hEnergy).isFailure())
  return StatusCode::FAILURE;

// In execute():
for (const auto& p : *inputCollection) {
  m_hEnergy->Fill(p.getEnergy());
}
```

In the steering file, configure `THistSvc`:
```python
from Configurables import THistSvc
histsvc = THistSvc()
histsvc.Output = ["output DATAFILE='output.root' OPT='RECREATE'"]
```

---

## 6. CMakeLists.txt Pattern

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

## 7. Python Steering File

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

## 8. Common EDM4hep Types

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

## 9. Project Directory Structure

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
