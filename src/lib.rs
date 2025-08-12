use gdnative::prelude::*;
use gdnative::api::{Spatial, Node};
use rand::Rng;
use std::collections::HashMap;

#[derive(NativeClass)]
#[inherit(Spatial)]
#[user_data(gdnative::export::user_data::MutexData<WeaveLangNative>)]
pub struct WeaveLangNative {
    owner: Ref<Spatial>,
    world_physics: HashMap<String, f32>,
    lab_nodes: HashMap<String, Ref<Node>>,
}

#[methods]
impl WeaveLangNative {
    fn new(owner: &Spatial) -> Self {
        WeaveLangNative {
            owner: unsafe { owner.assume_shared() },
            world_physics: HashMap::new(),
            lab_nodes: HashMap::new(),
        }
    }

    #[method]
    fn _ready(&mut self, #[base] owner: &Spatial) {
        self.lab_nodes.insert("accelerator".to_string(), owner.get_node("Accelerator").unwrap());
        self.lab_nodes.insert("chemistry_lab".to_string(), owner.get_node("ChemistryLab").unwrap());
        self.lab_nodes.insert("observatory".to_string(), owner.get_node("Observatory").unwrap());
        self.lab_nodes.insert("neuroscience_lab".to_string(), owner.get_node("NeuroscienceLab").unwrap());
        self.world_physics.insert("gravity".to_string(), 9.81);
    }

    #[method]
    fn _process(&mut self, #[base] _owner: &Spatial, _delta: f64) {
        let coherence = rand::thread_rng().gen_range(0.0..1.0);
        let risk = self.check_safety();
        if risk > 0.1 {
            godot_print!("Safety violation detected: {}", risk);
        } else {
            godot_print!("Coherence level: {}", coherence);
        }
    }

    #[method]
    fn design_experiment(&mut self, priority: f32) {
        godot_print!("Designing experiment with priority: {}", priority);
    }

    #[method]
    fn optimize_equipment(&mut self, efficiency: f32) {
        self.world_physics.insert("equipment_efficiency".to_string(), efficiency);
    }

    #[method]
    fn run_accelerator(&mut self) -> f32 {
        self.world_physics.get("gravity").unwrap_or(&9.81) + rand::thread_rng().gen_range(-0.1..0.1)
    }

    #[method]
    fn run_chemical_assay(&mut self) -> f32 {
        0.8 + rand::thread_rng().gen_range(-0.2..0.2)
    }

    #[method]
    fn run_neural_scan(&mut self) -> f32 {
        let risk = rand::thread_rng().gen_range(0.0..0.2);
        if risk > 0.1 {
            godot_print!("Safety violation detected: {}", risk);
        }
        risk
    }

    #[method]
    fn adjust_telescope(&mut self) {
        godot_print!("Adjusting telescope");
    }

    #[method]
    fn halt_experiment(&mut self) {
        godot_print!("Halting experiment due to safety violation");
    }

    #[method]
    fn check_safety(&self) -> f32 {
        rand::thread_rng().gen_range(0.0..0.2)
    }
}

fn init(handle: InitHandle) {
    handle.add_class::<WeaveLangNative>();
}

godot_init!(init);