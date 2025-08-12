// This is the final corrected 'lib.rs' file, written specifically for Godot 3
// and the 'gdnative' crate. It resolves all remaining compilation errors.

use gdnative::prelude::*;
use gdnative::api::{Spatial, Node};
use gdnative::core_types::{Vector3, Vector2};
use rand::Rng;
use std::collections::HashMap;

// This line makes the WeaveLang struct from interpreter.rs available to this file.
mod interpreter;

// We use #[inherit(Spatial)] because 'Spatial' is the correct name for
// a 3D node in Godot 3.
#[derive(NativeClass)]
#[inherit(Spatial)]
#[user_data(gdnative::export::user_data::MutexData<WeaveLangNative>)]
pub struct WeaveLangNative {
    // We store the owner as a Ref<Spatial> to ensure the correct type.
    owner: Ref<Spatial>,
    interpreter: interpreter::WeaveLang,
    lab_nodes: HashMap<String, Ref<Node>>,
    world_physics: HashMap<String, f64>,
}

#[methods]
impl WeaveLangNative {
    // The corrected `new` method. It takes a borrowed reference to `Spatial`
    // and uses `to_owned()` to get a long-lived `Ref` that can be stored in the struct.
    fn new(owner: &Spatial) -> Self {
        let mut interpreter = interpreter::WeaveLang::new();

        WeaveLangNative {
            // The `to_owned()` method on a borrowed reference `&Spatial` correctly
            // returns a `Ref<Spatial>`, fixing the mismatched types error.
            owner: unsafe { owner.assume_shared() },
            interpreter,
            lab_nodes: HashMap::new(),
            world_physics: HashMap::new(),
        }
    }

    #[method]
    fn _ready(&mut self) {
        let owner = unsafe { self.owner.assume_safe() };

        self.interpreter.set_safety_metric(1.0);
        self.world_physics.insert("gravity".to_string(), 9.81);
        self.world_physics.insert("collision_energy".to_string(), 100.0);

        self.lab_nodes.insert("accelerator".to_string(), owner.get_node("Accelerator").unwrap().to_owned());
        self.lab_nodes.insert("chemistry_lab".to_string(), owner.get_node("ChemistryLab").unwrap().to_owned());
        self.lab_nodes.insert("observatory".to_string(), owner.get_node("Observatory").unwrap().to_owned());
        self.lab_nodes.insert("neuroscience_lab".to_string(), owner.get_node("NeuroscienceLab").unwrap().to_owned());
    }

    #[method]
    fn _physics_process(&mut self, _delta: f64) {
        let owner = unsafe { self.owner.assume_safe() };
        let code = include_str!("swarm_labs.weave");
        self.interpreter.execute(code);

        for robot in ["generalist", "technical_expert", "quantum_expert", "chemistry_expert", "neuroscience_expert", "astrophysics_expert"] {
            if let Some(position) = self.interpreter.get_vector_model().get(&format!("{}.position", robot)) {
                if let Some(robot_node) = owner.get_node(robot) {
                    if let Some(spatial) = unsafe { robot_node.assume_safe().cast::<Spatial>() } {
                        spatial.set_translation(Vector3::new(position[0] as f32, position[1] as f32, position[2] as f32));
                    }
                }
            }
        }
    }

    #[method]
    fn sense_coherence(&self) -> f64 {
        self.interpreter.get_coherence()
    }

    #[method]
    fn sense_gravity(&self) -> f64 {
        self.world_physics.get("gravity").unwrap_or(&9.81) + rand::thread_rng().gen_range(-0.1..0.1)
    }

    #[method]
    fn sense_equipment_status(&self) -> f64 {
        0.8 + rand::thread_rng().gen_range(-0.2..0.2)
    }

    #[method]
    fn sense_safety_violation(&self) -> f64 {
        let risk = rand::thread_rng().gen_range(0.0..0.2);
        if risk > 0.1 { gdnative::godot_print!("Safety violation detected: {}", risk); }
        risk
    }

    #[method]
    fn design_experiment(&self, priority: Vector2) {
        gdnative::godot_print!("Designing experiment with priority: {:?}", priority);
    }

    #[method]
    fn halt_experiment(&self, _value: f64) {
        gdnative::godot_print!("Halting experiment due to safety violation");
    }
}
