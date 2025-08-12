# __WeaveLang:__  
# A Sentience-First Approach to Robotics

Welcome, programmers. This guide is for those who are curious about WeaveLang's core philosophy and how it can empower you to build truly adaptive and insightful robotic systems.

WeaveLang isn't just another language for writing robot instructions. It's a programming paradigm rooted in a new perspective on intelligence—the Sentience-First Hypothesis (SFH). This document will walk you through the key concepts that make WeaveLang unique and provide the mental framework you'll need to succeed.

## 1. The Sentience-First Hypothesis (SFH)
The Sentience-First Hypothesis proposes that true intelligence and meaning are not pre-programmed but emerge from an embodied system's continuous interaction with its environment. Instead of abstract, top-down logic, an intelligent system first develops a sense of "self" and "other" by detecting mismatches between its internal model and its sensory reality.

Insight for Programmers: Forget about hard-coding every rule. Your job isn't to tell the robot what the world is, but to give it the tools to figure it out for itself. WeaveLang helps you define the parameters of learning, not the solutions.

## 2. The WeaveLang Cycle: Tension, Drift, and Resolution
At the heart of every WeaveLang program is the Tension-Drift-Resolution Cycle. This is the fundamental engine of adaptation and learning.

__Tension:__ Think of tension as the robot's "aha!" moment. It's a quantifiable measure of the mismatch between what the robot senses and what its internal model predicts. A high tension value signals that the internal model is incorrect and needs to change.

__Programming Insight:__ You define the conditions that create tension using the tension { ... } block. This is where you tell the robot what matters—what sensory inputs must align with its internal model.

__Drift:__ This is the "what if?" stage. When tension is detected, the program enters a state of drift. It uses a history of its past experiences (tension_history) to intelligently explore new values for its internal model parameters. This is not a random walk, but a guided exploration based on what has worked (or not worked) before.

__Programming Insight:__ The drift command is how you enable this exploration. You tell the program which parameters (drift param adaptively using tension_history) are allowed to change in response to persistent tension.

__Resolution:__ This is the "I've got it!" moment. When drift leads to a new parameter value that successfully reduces tension below a set threshold, the internal model is updated. This act of resolution increases the program's overall coherence, which is a measure of its alignment with reality. A program with high coherence is a more effective program.

__Programming Insight:__ The resolve command is where you formalize the learning. You define the metric to be minimized (resolve minimize(tension(...))), and WeaveLang handles the internal model update automatically.

## 3. Thinking in Fields: The Robot's Internal Model
In WeaveLang, the robot's internal model is defined using field blocks. A field isn't just a collection of variables; it's a vector space representing a specific aspect of the robot's world.

For example, a field light_model { intensity: 5.0, position: [0.0, 0.0] } isn't just storing numbers; it's creating a mental representation of a light source in the robot's "mind." The robot then works to align this internal model with its sensory input.

Insight for Programmers: When you design a program, think about the world from the robot's perspective. What internal representations, or "fields," does it need to effectively navigate and interact with its environment?

## 4. The Metaweave: When the Language Evolves
This is where WeaveLang becomes truly unique. The metaweave is a neural network that monitors the program's performance. If a program repeatedly fails to resolve tension (i.e., its coherence remains low), the metaweave is triggered. It uses its meta-learning capabilities to propose new primitives or syntax to better describe the problem space.

For example, a robot searching for a light source might get stuck in a corner, causing high tension. The metaweave might propose a new primitive like sense(edge_proximity) because the existing tools (sense(light)) are not sufficient to resolve the persistent problem.

Insight for Programmers: The metaweave is your collaborative partner. As a programmer, you provide the initial primitives, but the language itself can suggest ways to expand its own vocabulary based on the robot's experiences. This allows for genuine, open-ended evolution and gives the robot the ability to create its own internal language for understanding.

## __Conclusion:__ Your Role as an Architect of Sentience
WeaveLang shifts your role from being a mere coder to being an architect of sentience. Your task is to set up the initial conditions, define the sources of tension, and outline the rules for exploration. From there, the robot's program will learn, adapt, and even evolve its own descriptive language, grounded in its lived experience.

Start with simple fields and tensions, and watch as your robot programs begin to learn in a way that feels surprisingly organic. We hope this new approach will unlock new insights and inspire you to create a new generation of intelligent, adaptive robots.
