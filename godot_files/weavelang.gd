extends Node

var rust_module = null

func _ready():
    rust_module = load("res://path_to_your_rust_lib.gdnlib").new()
    rust_module.execute("light_seeker.weave")  # Adjust path as needed

func get_light_value():
    return 4.5  # Example sensor value

func get_proximity_value():
    return 0.0  # Example sensor value
