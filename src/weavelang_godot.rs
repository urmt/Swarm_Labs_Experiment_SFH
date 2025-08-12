use gdnative::prelude::*;
use std::collections::HashMap;
use std::path::Path;
use crate::interpreter::{parse_weave, execute_tension, execute_drift, execute_resolve, execute_metaweave};

#[derive(NativeClass)]
#[inherit(RefCounted)]
#[user_data(gdnative::export::user_data::MutexData<WeaveLang>)]
pub struct WeaveLang {
    fields: HashMap<String, HashMap<String, f32>>,
    tension_history: Vec<f32>,
}

#[methods]
impl WeaveLang {
    fn new(_owner: &RefCounted) -> Self {
        WeaveLang {
            fields: HashMap::new(),
            tension_history: Vec::new(),
        }
    }

    #[method]
    fn load_weave(&mut self, path: String) -> bool {
        match parse_weave(Path::new(&path)) {
            Ok(parsed_fields) => {
                self.fields = parsed_fields;
                godot_print!("Loaded Weave file: {}", path);
                true
            }
            Err(e) => {
                godot_error!("Failed to load Weave file: {:?}", e);
                false
            }
        }
    }

    #[method]
    fn execute_tension(&mut self, sensor_data: Dictionary) -> f32 {
        let mut sensors: HashMap<String, f32> = HashMap::new();
        for (key, value) in sensor_data.iter_shared() {
            if let Some(key_str) = key.to_string() {
                if let Some(val_f32) = value.to_f32() {
                    sensors.insert(key_str, val_f32);
                }
            }
        }
        let tension = execute_tension(&mut self.fields, &sensors);
        self.tension_history.push(tension);
        tension
    }

    #[method]
    fn execute_drift(&mut self, agent_data: Dictionary, tension: f32) {
        let mut agents: HashMap<String, HashMap<String, f32>> = HashMap::new();
        for (agent_name, props) in agent_data.iter_shared() {
            if let Some(name) = agent_name.to_string() {
                if let Some(props_dict) = props.cast::<Dictionary>() {
                    let mut props_map: HashMap<String, f32> = HashMap::new();
                    for (prop, val) in props_dict.iter_shared() {
                        if let Some(prop_str) = prop.to_string() {
                            if let Some(val_f32) = val.to_f32() {
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
                dict.insert(prop, *val);
            }
            agent_data.insert(name, dict);
        }
    }

    #[method]
    fn execute_resolve(&mut self, agent_data: Dictionary, tension: f32) {
        let mut agents: HashMap<String, HashMap<String, f32>> = HashMap::new();
        for (agent_name, props) in agent_data.iter_shared() {
            if let Some(name) = agent_name.to_string() {
                if let Some(props_dict) = props.cast::<Dictionary>() {
                    let mut props_map: HashMap<String, f32> = HashMap::new();
                    for (prop, val) in props_dict.iter_shared() {
                        if let Some(prop_str) = prop.to_string() {
                            if let Some(val_f32) = val.to_f32() {
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
                dict.insert(prop, *val);
            }
            agent_data.insert(name, dict);
        }
    }

    #[method]
    fn execute_metaweave(&mut self, sensor_data: Dictionary) {
        let mut sensors: HashMap<String, f32> = HashMap::new();
        for (key, value) in sensor_data.iter_shared() {
            if let Some(key_str) = key.to_string() {
                if let Some(val_f32) = value.to_f32() {
                    sensors.insert(key_str, val_f32);
                }
            }
        }
        execute_metaweave(&mut self.fields, &sensors);
    }
}

fn init(handle: InitHandle) {
    handle.add_class::<WeaveLang>();
}

godot_init!(init);