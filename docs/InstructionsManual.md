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

# Example: Swarm Labs Triangular Formation

## This program (`swarm_labs.weave`) coordinates three agents into a triangular formation, adjusting their positions to maintain specific distances and responding to wind:

```weave
field agent1 {
  position: [0.0, 0.0],
  target_distance: 1.0
}
field agent2 {
  position: [1.0, 0.5],
  target_distance: 1.0
}
field agent3 {
  position: [0.5, -0.5],
  target_distance: 1.0
}

tension {
  sense(distance, agent1, agent2) > target_distance => act(move_toward, agent1, agent2);
  sense(distance, agent2, agent3) > target_distance => act(move_toward, agent2, agent3);
  sense(distance, agent3, agent1) > target_distance => act(move_toward, agent3, agent1)
}

drift agent1.target_distance adaptively using tension_history
drift agent2.target_distance adaptively using tension_history
drift agent3.target_distance adaptively using tension_history

constrain tension(sense(distance, agent1, agent2), agent1.target_distance) < 1.5
constrain tension(sense(distance, agent2, agent3), agent2.target_distance) < 1.5
constrain tension(sense(distance, agent3, agent1), agent3.target_distance) < 1.5

resolve minimize(tension(sense(distance, agent1, agent2), agent1.target_distance))
resolve minimize(tension(sense(distance, agent2, agent3), agent2.target_distance))
resolve minimize(tension(sense(distance, agent3, agent1), agent3.target_distance))

metaweave define sense_wind as sense(wind_sensor)

extend field agent1 with wind_speed: 0.0 when sense(wind_sensor) > 0
extend field agent2 with wind_speed: 0.0 when sense(wind_sensor) > 0
extend field agent3 with wind_speed: 0.0 when sense(wind_sensor) > 0

loop 10 {
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
- **field**: Defines each agent’s starting position and target distance (1.0 unit) for the triangular formation.
- **tension**: Moves agents closer if their distance exceeds the target distance, forming a triangle (agent1 to agent2, agent2 to agent3, agent3 to agent1).
- **drift**: Adjusts each agent’s `target_distance` dynamically based on past tension data to optimize the formation.
- **constrain**: Keeps the tension (distance deviation) below 1.5 units for stable coordination.
- **metaweave**: Defines a `sense_wind` primitive using a neural network to detect wind conditions.
- **extend field**: Adds a `wind_speed` property to each agent if wind is detected (via `wind_sensor`).
- **loop**: Runs the tension, drift, resolve, and metaweave steps 10 times, applying metaweave only if tension exceeds 2.0.

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
