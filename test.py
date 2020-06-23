import arena
arena.init("oz.andrew.cmu.edu", "realm", "kaichieh1")
basketballStand = arena.Object(objType=arena.Shape.gltf_model,
    location=(0, -0.35, 0),
    rotation=(0,0,0,0),
    scale=(0.01, 0.01, 0.01),
    url="https://rawcdn.githack.com/kaichiehuang/Arena/3ff149db669fd06ee05ed7b542faad1bd85a6ee8/3Dmodels/basketballStand.glb?raw=true")


basketball = arena.Object(objType=arena.Shape.gltf_model,
    scale=(0.1, 0.1, 0.1),
    location=(0, 2, 0),
    url="https://rawcdn.githack.com/kaichiehuang/Arena/908cc639306670e595a06b21e13d37c5cb66c29f/3Dmodels/basketball.glb?raw=true")

basketball.update(physics=arena.Physics.dynamic)


arena.handle_events()
    