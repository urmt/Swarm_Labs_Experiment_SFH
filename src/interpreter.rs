use gdnative::prelude::*;
use pest::Parser;
use pest_derive::Parser;
use std::collections::HashMap;
use std::path::Path;

#[derive(Parser)]
#[grammar = "weavelang.pest"]
pub struct WeaveLangParser;

pub fn parse_weave(path: &Path) -> Result<HashMap<String, HashMap<String, f32>>, pest::error::Error<Rule>> {
    let code = std::fs::read_to_string(path).map_err(|e| pest::error::Error::<Rule>::new_from_span(
        pest::error::ErrorVariant::CustomError { message: e.to_string() },
        pest::Span::new("", 0, 0).unwrap(),
    ))?;
    let pairs = WeaveLangParser::parse(Rule::file, &code)?;
    let mut fields = HashMap::new();
    for pair in pairs {
        match pair.as_rule() {
            Rule::field => {
                let mut field_data = HashMap::new();
                let mut field_name = String::new();
                for inner in pair.into_inner() {
                    match inner.as_rule() {
                        Rule::ident => field_name = inner.as_str().to_string(),
                        Rule::field_param => {
                            let mut param_name = String::new();
                            let mut param_value = 0.0;
                            for param in inner.into_inner() {
                                match param.as_rule() {
                                    Rule::ident => param_name = param.as_str().to_string(),
                                    Rule::number => param_value = param.as_str().parse::<f32>().unwrap_or(0.0),
                                    _ => {}
                                }
                            }
                            field_data.insert(param_name, param_value);
                        }
                        _ => {}
                    }
                }
                fields.insert(field_name, field_data);
            }
            _ => {}
        }
    }
    godot_print!("Executing WeaveLang code: {}", path.display());
    Ok(fields)
}

pub fn execute_tension(fields: &mut HashMap<String, HashMap<String, f32>>, sensors: &HashMap<String, f32>) -> f32 {
    let coherence = sensors.get("coherence").unwrap_or(&0.0);
    let generalist_coherence = fields.get("generalist").unwrap().get("coherence_target").unwrap_or(&0.5);
    let tension = (coherence - generalist_coherence).abs();
    godot_print!("Tension calculated: {}", tension);
    tension
}

pub fn execute_drift(fields: &mut HashMap<String, HashMap<String, f32>>, agents: &HashMap<String, HashMap<String, f32>>, history: &[f32], tension: f32) {
    for (agent_name, props) in agents {
        if let Some(field) = fields.get_mut(agent_name) {
            if let Some(target) = field.get_mut("coherence_target").or_else(|| field.get_mut("physics_constant")) {
                *target += tension * 0.01;
            }
        }
    }
}

pub fn execute_resolve(fields: &mut HashMap<String, HashMap<String, f32>>, agents: &HashMap<String, HashMap<String, f32>>, tension: f32) {
    for (agent_name, props) in agents {
        if let Some(field) = fields.get_mut(agent_name) {
            if let Some(target) = field.get_mut("coherence_target").or_else(|| field.get_mut("physics_constant")) {
                *target -= tension * 0.005;
            }
        }
    }
}

pub fn execute_metaweave(fields: &mut HashMap<String, HashMap<String, f32>>, sensors: &HashMap<String, f32>) {
    if sensors.get("gravity_sensor").unwrap_or(&0.0) > 0.0 {
        fields.get_mut("quantum_expert").unwrap().insert("gravity".to_string(), 9.81);
    }
    godot_print!("Metaweave executed");
}