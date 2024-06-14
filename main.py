
import math
import numpy as np
from simpub import SimPublisher, MJCFScene
import mujoco as mj

from simpub.simdata import UnityJointType
from simpub.transform import quat2euler

scene = MJCFScene.from_file("scenes/agility_cassie/scene.xml")

publisher = SimPublisher(scene)

model : mj._structs.MjModel = mj.MjModel.from_xml_string(scene.xml_string, scene.xml_assets)
data : mj._structs.MjData = mj.MjData(model)
# REVIEW: I suggest to use the SimPublisher to track them automatically
# and also usrs can specify joints they want or don't want to track
for joint in scene.worldbody.get_joints({UnityJointType.HINGE}):
    mjjoint = data.joint(joint.name)
    publisher.track_joint(joint.name, (mjjoint,), lambda x: np.degrees([x.qpos[0], x.qvel[0]]))

for joint in scene.worldbody.get_joints({UnityJointType.SLIDE}):
    mjjoint = data.joint(joint.name)
    publisher.track_joint(joint.name, (mjjoint,), lambda x: np.concatenate([x.qpos, x.qvel]))

for joint in scene.worldbody.get_joints({UnityJointType.BALL}):
    mjjoint = data.joint(joint.name)
    publisher.track_joint(joint.name, (mjjoint,), lambda x: np.concatenate([quat2euler(x.qpos), x.qvel]))




publisher.start()

mj.mj_resetDataKeyframe(model, data, 0)

mj.mj_forward(model,data)
while True:
  mj.mj_step(model, data)
  
publisher.shutdown()
