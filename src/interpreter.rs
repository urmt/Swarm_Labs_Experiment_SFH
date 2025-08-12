use std::collections::HashMap;

pub struct WeaveLang {
    model: HashMap<String, f64>,
    vector_model: HashMap<String, Vec<f64>>,
    coherence: f64,
}

impl WeaveLang {
    pub fn new() -> Self {
        WeaveLang {
            model: HashMap::new(),
            vector_model: HashMap::new(),
            coherence: 0.0,
        }
    }

    pub fn execute(&mut self, code: &str) {
        gdnative::godot_print!("Executing WeaveLang code: {}", code);
    }

    // Public methods to access private fields
    pub fn set_safety_metric(&mut self, value: f64) {
        self.model.insert("generalist.safety_metric".to_string(), value);
    }

    pub fn get_vector_model(&self) -> &HashMap<String, Vec<f64>> {
        &self.vector_model
    }

    pub fn get_coherence(&self) -> f64 {
        self.coherence
    }
}
