# WeaveLang Specification

## Overview
WeaveLang is a programming language for computer-robots, inspired by the Sentience-First Hypothesis (SFH). It encodes tension (mismatches between model and reality), coherence (alignment via resolution), and self-updating significance through interaction, per SFH Chapter 30. Programs evolve through a tension-drift-resolution cycle, interacting with a virtual world (e.g., Godot).

## Syntax
- **Field**: Defines the internal model as a vector space.  
  Syntax: `field model_name { param: value, ... }`  
  Example: `field light_model { intensity: 5.0, position: [0.0, 0.0] }`
- **Tension**: Detects mismatches between sensed and expected states.  
  Syntax: `tension { condition => action; ... }`  
  Example: `tension { sense(light) < intensity => act(move, [0.1, 0.1]) }`
- **Drift**: Explores model adjustments adaptively.  
  Syntax: `drift param adaptively using tension_history`  
  Example: `drift intensity adaptively using tension_history`
- **Resolve**: Updates the model to minimize tension.  
  Syntax: `resolve minimize(tension(sense(sensor), param))`  
  Example: `resolve minimize(tension(sense(light), intensity))`
- **Constrain**: Ensures stability by limiting drift.  
  Syntax: `constrain metric < threshold`  
  Example: `constrain tension(sense(light), intensity) < 2.0`
- **Metaweave**: Proposes new primitives or syntax.  
  Syntax: `metaweave define primitive_name as action`  
  Example: `metaweave define sense_proximity as sense(proximity_sensor)`
- **Extend Field**: Adds new parameters to the model.  
  Syntax: `extend field model_name with param: value when condition`  
  Example: `extend field light_model with proximity: 0.0 when sense(proximity_sensor) > 0`
- **Loop**: Repeats execution cycles.  
  Syntax: `loop count { statements }`  
  Example: `loop 10 { execute tension }`

## Semantics
- **Tension-Drift-Resolution Cycle**:  
  1. **Tension**: Compute mismatch (e.g., `|sense(light) - intensity|`).  
  2. **Drift**: Perturb parameters using history-based ranges.  
  3. **Resolution**: Update model if tension is below threshold, increasing coherence.  
- **Field-Based Execution**: Models are vector spaces, updated dynamically.  
- **Self-Evolution**: `metaweave` and `extend field` enable new primitives and parameters based on interaction patterns.

## Runtime Environment
- **Interpreter**: Parses and executes WeaveLang, monitoring coherence.  
- **Godot Integration**: Maps `sense`/`act` to Godot nodes (e.g., `PointLight3D` for light).  
- **Meta-Field**: Tracks interactions and proposes syntax updates via a neural network.

## Example
See `examples/light_seeker.weave` for a robot navigating toward a light source, evolving its model through interaction.
