# WeaveLang - Sentience Programming Language

WeaveLang is a domain-specific language (DSL) for programming robots that does something special: it's designed around the Sentience-First Hypothesis (SFH), where a program's meaning is grounded in its real-world interaction, not just a static set of symbolic instructions. The language's core concepts are specifically built to enable a robot to adapt and evolve its internal model dynamically. It isn't just a layer of wasted effort; it's a novel, albeit experimental, approach to embodied cognition and programming for robotics.


## Core Concepts and Functionality
WeaveLang's programs are not linear sets of commands but rather define a tension-drift-resolution cycle that the robot executes. This cycle allows the program to respond to unexpected events and change its own behavior:

__Tension:__ This is the core mechanism for detecting a mismatch between a robot's internal model (its "expectations") and the data it receives from its sensors. The syntax tension { sense(...) < value => act(...) } explicitly links a sensory observation to an action triggered by a mismatch.

__Drift:__ When tension is high, the program enters a "drift" state, where it adaptively explores and perturbs its internal model parameters. This is a form of adaptive exploration, allowing the robot to try new behaviors or interpretations of its world.

__Resolution:__ This is the model-updating phase. If a drift adjustment leads to a reduction in tension, the new model parameter is adopted, increasing the system's "coherence". This process is governed by a constrain command, which ensures stability by limiting the drift range.

__Metaweave:__ This is perhaps the most innovative feature. It's a neural network-driven mechanism that allows the program to propose and create new primitives or syntax in real-time. For example, if a robot encounters wind, the metaweave might propose a new sense_wind primitive and add a wind_speed parameter to its internal model. This allows the robot to dynamically adapt to new sensors or environmental factors without needing to be re-coded.



## How it Works
The language is implemented as an interpreter written in Rust, which handles the parsing and execution of the code. The interpreter is designed to be integrated with Godot 4.3, a game engine that provides the virtual environment and physics for the robots. The sense and act commands in WeaveLang map directly to the sensors and actuators of the robots within the Godot environment.

An example program for a light-seeking robot shows this loop in action. The robot starts with a model that expects a certain light intensity. When the sensed light is lower or higher, tension is created, which prompts the program to move the robot. As the robot gets closer, the internal model updates to a new expected light value, increasing coherence and allowing it to adapt to its environment. The weavelang_godot.rs file shows how a robot's position in the Godot environment is updated based on the interpreter's internal vector model.

## Comparison to Other Languages
Unlike traditional programming languages that require a programmer to explicitly define every possible behavior and state transition, WeaveLang allows a robot's behavior to emerge from its interaction with the environment. Instead of simply following a pre-defined path to a light source, a WeaveLang program would evolve its own definition of "light-seeking" based on the sensor feedback and the tension-drift-resolution cycle.

While it shares some similarities with declarative languages or even some reactive programming paradigms, its explicit focus on dynamic model evolution, grounding meaning in interaction, and the use of a neural network for self-modification (metaweave) sets it apart as a tool for developing truly adaptive, rather than just responsive, robotic systems.
