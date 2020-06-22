import arena
arena.init("oz.andrew.cmu.edu", "realm", "kaichieh1")
cybertruck = arena.Object(objType=arena.Shape.gltf_model,
    scale=(0.1, 0.1, 0.1),
    location=(0, 0, 0),
    url="https://xr.andrew.cmu.edu/models/cybertruck/scene.gltf")

cybertruck.update(data='{"animation-mixer": {"clip": "*"}}')

# cybertruck = arena.Object(
#     objName="cybertruck",
#     objType=arena.Shape.gltf_model,
#     location=(0, 3, 0.4),
#     scale=(0.1, 0.1, 0.01),
#     url="https://xr.andrew.cmu.edu/models/AnimatedTriangle.gltf"
# )
#cybertruck.update(data='{"animation-mixer": {"clip": "*"}}')
# cow = arena.Object(
#     objName="model2",
#     objType=arena.Shape.gltf_model,
#     location=(-21, 1.8, -8),
#     scale=(0.02, 0.02, 0.02),
#     url="https://xr.andrew.cmu.edu/models/cow2/scene.gltf",
# )

arena.handle_events()
    