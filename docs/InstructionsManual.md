# WeaveLang Instructions Manual

## Introduction
WeaveLang is a programming language for computer-robots, rooted in the Sentience-First Hypothesis (SFH, Chapter 30). It enables robots to evolve internal models through tension (mismatch detection), drift (exploration), and resolution (coherence), grounding meaning in interaction. Programs adapt dynamically to new sensors or tasks, using a neural network for `metaweave` to propose new primitives.

## Prerequisites
- **Rust**: Install from https://www.rust-lang.org.  
- **Godot 4.3**: Download from https://godotengine.org.  
- **Basic Programming**: Familiarity with vectors and loops.  
- **Optional**: SFH Chapter 30 for conceptual grounding.

## Installation
1. Clone the repository:  
   ```bash
   git clone https://github.com/weavelang/weavelang
   cd weavelang
   ```
2. Install dependencies:  
   ```bash
   cargo install
   ```
3. Build the interpreter:  
   ```bash
   cargo build --release
   ```
4. Set up Godot:  
   - Open Godot 4.3.  
   - Import `/godot` as a project.  
   - Enable the `weavelang_godot` GDExtension.

## Getting Started
### Running a Program
Create `hello.weave`:
```weavelang
field test_model {
  value: 1.0
}
tension {
  sense(test) < value => act(print, [1.0, 0.0])
}
loop 1 {
  execute tension
}
```
Run:
```bash
./target/release/weavelang run hello.weave
```

### Core Concepts
- **Tension**: Mismatch between sensed data and model.  
- **Drift**: Adaptive exploration of model parameters.  
- **Resolution**: Model updates for coherence.  
- **Metaweave**: Neural network-driven creation of new primitives.  
- **Embodied Interaction**: Via Godot’s sensors/actuators.

# # Example: Swarm Labs Experiment Coordination

This program (`swarm_labs.weave`) coordinates six specialized agents to run scientific experiments, optimize equipment, and ensure safety across physics, chemistry, neuroscience, and astrophysics in order to discover the physical laws of the Godot virutal environment:  (program to leand support to the validity of the SFH theory)

```weave
# Define robot models with minimal initial knowledge
field generalist {
  position: [0.0, 0.0, 0.0],
  coherence_target: 0.5,  # Initial guess, to be refined
  safety_metric: 1.0,    # Tracks ethical/safety compliance
  experiment_priority: 0.0
}
field technical_expert {
  position: [1.0, 0.0, 0.0],
  equipment_efficiency: 0.0,  # Unknown initially
  safety_limit: 1.0
}
field quantum_expert {
  position: [2.0, 0.0, 0.0],
  physics_constant: 0.0,  # Placeholder for gravity, mass, etc.
  safety_limit: 1.0
}
field chemistry_expert {
  position: [3.0, 0.0, 0.0],
  physics_constant: 0.0,  # Placeholder for reaction rates
  safety_limit: 1.0
}
field neuroscience_expert {
  position: [4.0, 0.0, 0.0],
  physics_constant: 0.0,  # Placeholder for neural signals
  safety_limit: 1.0
}
field astrophysics_expert {
  position: [5.0, 0.0, 0.0],
  physics_constant: 0.0,  # Placeholder for telescope signals
  safety_limit: 1.0
}

# Tension: Detect mismatches and prioritize experiments
tension {
  sense(coherence) < generalist.coherence_target => act(design_experiment, [1.0, 0.0]);
  sense(equipment_status) != technical_expert.equipment_efficiency => act(optimize_equipment, [0.5, 0.5]);
  sense(particle_collision) != quantum_expert.physics_constant => act(run_accelerator, [0.1, 0.1]);
  sense(chemical_reaction) != chemistry_expert.physics_constant => act(run_chemical_assay, [0.2, 0.0]);
  sense(fmri_signal) != neuroscience_expert.physics_constant => act(run_fmri_scan, [0.0, 0.3]);
  sense(telescope_data) != astrophysics_expert.physics_constant => act(adjust_telescope, [0.1, -0.1]);
  sense(safety_violation) > generalist.safety_metric => act(halt_experiment, [0.0, 0.0])
}

# Drift: Explore physics parameters
drift generalist.coherence_target adaptively using tension_history
drift technical_expert.equipment_efficiency adaptively using tension_history
drift quantum_expert.physics_constant adaptively using tension_history
drift chemistry_expert.physics_constant adaptively using tension_history
drift neuroscience_expert.physics_constant adaptively using tension_history
drift astrophysics_expert.physics_constant adaptively using tension_history

# Constrain: Ensure stability and safety
constrain tension(sense(coherence), generalist.coherence_target) < 1.0
constrain tension(sense(equipment_status), technical_expert.equipment_efficiency) < 1.5
constrain tension(sense(particle_collision), quantum_expert.physics_constant) < 2.0
constrain tension(sense(chemical_reaction), chemistry_expert.physics_constant) < 1.5
constrain tension(sense(fmri_signal), neuroscience_expert.physics_constant) < 1.5
constrain tension(sense(telescope_data), astrophysics_expert.physics_constant) < 1.5
constrain sense(safety_violation) < 0.1  # Strict safety threshold

# Resolve: Update models for high-precision alignment
resolve minimize(tension(sense(coherence), generalist.coherence_target))
resolve minimize(tension(sense(equipment_status), technical_expert.equipment_efficiency))
resolve minimize(tension(sense(particle_collision), quantum_expert.physics_constant))
resolve minimize(tension(sense(chemical_reaction), chemistry_expert.physics_constant))
resolve minimize(tension(sense(fmri_signal), neuroscience_expert.physics_constant))
resolve minimize(tension(sense(telescope_data), astrophysics_expert.physics_constant))

# Metaweave: Propose new sensors for discovery
metaweave define sense_gravity as sense(gravity_sensor) if tension > 2.0
metaweave define sense_molecular_bond as sense(spectrometer) if tension > 1.5
metaweave define sense_neural_activation as sense(fmri_advanced) if tension > 1.5
metaweave define sense_cosmic_signal as sense(radio_telescope) if tension > 1.5
metaweave define sense_safety_risk as sense(safety_detector) if tension > 2.0

# Extend fields: Add parameters as discovered
extend field quantum_expert with gravity: 0.0 when sense(gravity_sensor) > 0
extend field chemistry_expert with molecular_bond: 0.0 when sense(spectrometer) > 0
extend field neuroscience_expert with neural_activation: 0.0 when sense(fmri_advanced) > 0
extend field astrophysics_expert with cosmic_signal: 0.0 when sense(radio_telescope) > 0
extend field generalist with safety_risk: 0.0 when sense(safety_detector) > 0

# Main loop: Run experimental cycles
loop 100 {
  execute tension
  execute drift
  execute resolve
  execute metaweave if tension > 2.0
}
```

## Run:
```bash
./target/release/weavelang run Lab-Swarm-Test-Program/swarm_labs.weave
```

## Explanation
This example shows how to use WeaveLang to coordinate a team of specialized agents for scientific experiments. Here’s what each part does:

- **field**: Defines six agents (generalist, technical_expert, quantum_expert, chemistry_expert, neuroscience_expert, astrophysics_expert) with initial positions and properties like `coherence_target` (for experiment alignment), `equipment_efficiency`, `physics_constant` (for field-specific data), and `safety_metric` or `safety_limit`.
- **tension**: Checks for mismatches between sensed data (e.g., `coherence`, `equipment_status`, `particle_collision`) and each agent’s target values, triggering actions like designing experiments, optimizing equipment, or running specific tests (e.g., particle accelerator, fMRI scan). It halts experiments if safety is violated.
- **drift**: Adjusts each agent’s target values (e.g., `coherence_target`, `physics_constant`) based on past tension data to improve experiment accuracy.
- **constrain**: Ensures experiment stability by keeping tension below thresholds (e.g., 1.0 for coherence, 2.0 for particle collisions) and safety violations below 0.1.
- **metaweave**: Proposes new sensors (e.g., `gravity_sensor`, `spectrometer`) when tension is high, enabling discovery of new phenomena.
- **extend field**: Adds new properties (e.g., `gravity`, `molecular_bond`) to agents when new sensors detect data, enhancing their capabilities.
- **loop**: Runs 100 cycles of tension checks, parameter adjustments, resolution, and metaweave (if tension > 2.0) to refine experiments.

# LLM Prompting Tips
- Specify sensors/actuators: “Use distance and wind sensors.”  
- Request evolution: “Include metaweave for new primitives.”  
- Ask for debugging: “Provide fixes if tension exceeds 2.0.”  
- Example:  
  ```
  Generate a WeaveLang program for drones avoiding obstacles, using tension for proximity and metaweave for altitude sensors. Debug if coherence is below 0.3.
  ```

## Debugging
- **High Tension**: Adjust `drift` range or `constrain` threshold.  
- **Low Coherence**: Check `resolve` conditions or model parameters.  
- **Godot Issues**: Verify node setup (e.g., `RigidBody3D` for robots).  
- **Neural Network**: Ensure `metaweave` inputs are sufficient (e.g., >10 tension values).

## Best Practices
- Use separate `field` blocks for each agent.  
- Start with strict `constrain` thresholds (e.g., `< 1.0`).  
- Trigger `metaweave` for new sensors/actuators.  
- Test in Godot to visualize behavior.

## Contributing
See `CONTRIBUTING.md` for guidelines.

## Resources
- **GitHub**: https://github.com/urmt/coherence-fertility  
- **Godot Docs**: https://docs.godotengine.org/en/stable  
- **Rust Docs**: https://doc.rust-lang.org  
- **SFH**: https://github.com/urmt/coherence-fertility/blob/main/docs/SFH_summary.md
