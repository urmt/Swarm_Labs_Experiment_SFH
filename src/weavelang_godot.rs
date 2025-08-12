use godot::prelude::*;
use std::collections::HashMap;
use std::path::Path;

// Assume interpreter.rs exports these
use crate::interpreter::{parse_weave, execute_tension, execute_drift, execute_resolve, execute_metaweave};

struct WeaveLangExtension;

#[gdextension]
unsafe impl ExtensionLibrary for WeaveLangExtension {}

#[derive(GodotClass)]
#[class(base=RefCounted)]
struct WeaveLang {
    fields: HashMap<String, HashMap<String, f32>>,
    tension_history: Vec<f32>,
}

#[godot_api]
impl RefCountedVirtual for WeaveLang {
    fn init(_base: Base<RefCounted>) -> Self {
        WeaveLang {
            fields: HashMap::new(),
            tension_history: Vec::new(),
        }
    }
}

#[godot_api]
impl WeaveLang {
    #[func]
    fn load_weave(&mut self, path: GString) -> bool {
        let path_str = path.to_string();
        match parse_weave(Path::new(&path_str)) {
            Ok(parsed_fields) => {
                self.fields = parsed_fields;
                godot_print!("Loaded Weave file: {}", path_str);
                true
            }
            Err(e) => {
                godot_error!("Failed to load Weave file: {:?}", e);
                false
            }
        }
    }

    #[func]
    fn execute_tension(&mut self, sensor_data: Dictionary) -> f32 {
        let mut sensors: HashMap<String, f32> = HashMap::new();
        for (key, value) in sensor_data.iter() {
            if let Ok(key_str) = key.try_to::<String>() {
                if let Ok(val_f32) = value.try_to::<f32>() {
                    sensors.insert(key_str, val_f32);
                }
            }
        }
        let tension = execute_tension(&mut self.fields, &sensors);
        self.tension_history.push(tension);
        tension
    }

    #[func]
    fn execute_drift(&mut self, agent_data: Dictionary, tension: f32) {
        let mut agents: HashMap<String, HashMap<String, f32>> = HashMap::new();
        for (agent_name, props) in agent_data.iter() {
            if let Ok(name) = agent_name.try_to::<String>() {
                if let Ok(props_dict) = props.try_to::<Dictionary>() {
                    let mut props_map: HashMap<String, f32> = HashMap::new();
                    for (prop, val) in props_dict.iter() {
                        if let Ok(prop_str) = prop.try_to::<String>() {
                            if let Ok(val_f32) = val.try_to::<f32>() {
                                props_map.insert(prop_str, val_f32);
                            }
                        }
                    }
                    agents.insert(name, props_map);
                }
            }
        }
        execute_drift(&mut self.fields, &agents, &self.tension_history, tension);
        for (name, props) in agents.iter() {
            let mut dict = Dictionary::new();
            for (prop, val) in props {
                dict.set(prop, *val);
            }
            agent_data.set(name, dict);
        }
    }

    #[func]
    fn execute_resolve(&mut self, agent_data: Dictionary, tension: f32) {
        let mut agents: HashMap<String, HashMap<String, f32>> = HashMap::new();
        for (agent_name, props) in agent_data.iter() {
            if let Ok(name) = agent_name.try_to::<String>() {
                if let Ok(props_dict) = props.try_to::<Dictionary>() {
                    let mut props_map: HashMap<String, f32> = HashMap::new();
                    for (prop, val) in props_dict.iter() {
                        if let Ok(prop_str) = prop.try_to::<String>() {
                            if let Ok(val_f32) = val.try_to::<f32>() {
                                props_map.insert(prop_str, val_f32);
                            }
                        }
                    }
                    agents.insert(name, props_map);
                }
            }
        }
        execute_resolve(&mut self.fields, &agents, tension);
        for (name, props) in agents.iter() {
            let mut dict = Dictionary::new();
            for (prop, val) in props {
                dict.set(prop, *val);
            }
            agent_data.set(name, dict);
        }
    }

    #[func]
    fn execute_metaweave(&mut self, sensor_data: Dictionary) {
        let mut sensors: HashMap<String, f32> = HashMap::new();
        for (key, value) in sensor_data.iter() {
            if let Ok(key_str) = key.try_to::<String>() {
                if let Ok(val_f32) = value.try_to::<f32>() {
                    sensors.insert(key_str, val_f32);
                }
            }
        }
        execute_metaweave(&mut self.fields, &sensors);
    }
}