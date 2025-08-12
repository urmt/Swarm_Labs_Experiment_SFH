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

## Example: Light-Seeking Robot
See `examples/light_seeker.weave` (previously provided). It navigates a robot toward a light source, evolving to handle a proximity sensor.

## Example: Swarm V-Formation
This program (`swarm_v_formation.weave`) coordinates three robots into a V-shape:
```weavelang
field robot1 {
  position: [0.0, 0.0],
  target_distance: 1.0
}
field robot2 {
  position: [1.0, 0.5],
  target_distance: 1.0
}
field robot3 {
  position: [1.0, -0.5],
  target_distance: 1.0
}

tension {
  sense(distance, robot1, robot2) > target_distance => act(move_toward, robot1, robot2);
  sense(distance, robot2, robot3) > target_distance => act(move_toward, robot2, robot3)
}

drift robot1.target_distance adaptively using tension_history
drift robot2.target_distance adaptively using tension_history
drift robot3.target_distance adaptively using tension_history

constrain tension(sense(distance, robot1, robot2), robot1.target_distance) < 1.5
constrain tension(sense(distance, robot2, robot3), robot2.target_distance) < 1.5

resolve minimize(tension(sense(distance, robot1, robot2), robot1.target_distance))
resolve minimize(tension(sense(distance, robot2, robot3), robot2.target_distance))

metaweave define sense_wind as sense(wind_sensor)

extend field robot1 with wind_speed: 0.0 when sense(wind_sensor) > 0
extend field robot2 with wind_speed: 0.0 when sense(wind_sensor) > 0
extend field robot3 with wind_speed: 0.0 when sense(wind_sensor) > 0

loop 10 {
  execute tension
  execute drift
  execute resolve
  execute metaweave if tension > 2.0
}
```
Run:
```bash
./target/release/weavelang run examples/swarm_v_formation.weave
```

### Explanation
- `field`: Defines each robot’s position and target distance.  
- `tension`: Adjusts positions if distances deviate from target.  
- `drift`: Explores `target_distance` adjustments.  
- `constrain`: Ensures stable coordination.  
- `metaweave`: Adds a `sense_wind` primitive via neural network.  
- `extend field`: Incorporates `wind_speed` if wind is detected.

## Using the Neural Network in Metaweave
The `metaweave` construct uses a neural network (`tch-rs`) to propose new primitives:
- **Input**: Last 10 tension values.  
- **Output**: Suggested primitive/action (e.g., `sense_wind as sense(wind_sensor)`).  
- **Training**: Updates weights when coherence exceeds 0.5, reinforcing successful primitives.  
- **Usage**: Trigger with `metaweave define auto as auto` for network-driven proposals.

Example:
```weavelang
metaweave define auto as auto
```
Output:
```
Neural network proposed: sense_wind as sense(wind_sensor)
```

## Using LLMs for WeaveLang
LLMs (e.g., Grok, ChatGPT) can generate and debug WeaveLang code provided you give it links to the github files or upload the files that explain how it functions and how to program it.

### General Projects
- **Prompt**:  
  ```
  Write a WeaveLang program for a robot swarm forming a grid, using tension for spacing and metaweave for new sensors.
  ```
- **Output**: Program with multiple `field` blocks and `metaweave` for dynamic sensors.

### Specific Projects
- **Prompt**:  
  ```
  Create a WeaveLang program for a robotic arm sorting objects by weight in Godot, with tension for grip strength and metaweave for color sensors. Suggest debugging if tension is high.
  ```
- **Output**: Program with `sense(weight)`, `act(grip)`, and debugging tips (e.g., tighten `constrain`).

### LLM Prompting Tips
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
