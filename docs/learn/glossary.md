# Glossary

Each term links to the chapter that explains it. The 中文 column gives the Chinese term people use. A dash marks
a name (LIBERO, PaliGemma, LoRA and so on), which stays in Latin letters; a blank means we haven't chosen a term yet.
The web pages show the same Chinese terms from `docs/assets/js/glossary.js`; the choices and their alternatives are in
`library/terms-zh.yaml`.

| Term | 中文 | Meaning | Chapter |
|---|---|---|---|
| action | 动作 | The numbers a policy outputs to move the robot. In LIBERO, seven: three for moving the hand, three for rotating it, one for the gripper. | 1 |
| attention | 注意力 | Inside a transformer, the step where each token looks at the others and takes in what they hold. In π0.5 the words reach the actions only this way. | 2 |
| action chunk | 动作块 | Several future actions predicted in one call. `pi05_libero` predicts 10, and the evaluation script runs 5 before asking again. | 1 |
| action expert | 动作专家 | The smaller network in π0 and π0.5 that turns noise into an action chunk while attending to the VLM's output. | 2 |
| behaviour cloning | 行为克隆 | Training a policy to copy what a human operator did in recorded demonstrations. | 1 |
| CAG | — | Counterfactual Action Guidance, from the LIBERO-CF paper. Runs the policy with and without the instruction and amplifies the difference. | 5 |
| checkpoint | 检查点 | A saved set of trained model weights, such as `pi05_libero`. | 2 |
| counterfactual instruction | 反事实指令 | A feasible instruction for a different task in a scene the model already knows. | 4, 5 |
| episode (trial) | 回合 | One run of the robot from a starting arrangement until success or the step limit. | 3 |
| faithful / biased success |  | Under a different-task instruction, whether the robot completed the new task (faithful) or the scene's original task (biased). | 4 |
| gradient | 梯度 | The signal training sends backwards through a network after each guess, telling every parameter which way to move. | 2 |
| fine-tuning | 微调 | Further training of a pretrained model on the tasks it will be tested on. | 1 |
| flow matching | 流匹配 | A way to generate continuous outputs by learning to move random noise, step by step, towards real data. π0 and π0.5 use it for actions. | 1, 2 |
| grounding (language grounding) |  | Our working definition: changing the words changes what the robot does, in the way the words say. | 4 |
| grounding rate |  | How often the gripper touches the object the instruction names, whether or not the task finishes. | 4 |
| image encoder | 图像编码器 | The part of a vision-language model that turns a picture into tokens; SigLIP in PaliGemma. | 2 |
| knowledge insulation | 知识隔离 | Stopping the action expert's training gradients from flowing into the VLM, so robot training doesn't erase the VLM's web knowledge. Used in pre-training `pi05_base`, not in openpi's fine-tuning. | 2 |
| LIBERO | — | A simulated benchmark of 130 manipulation tasks on a Franka Panda arm in MuJoCo. | 3 |
| LIBERO-Spatial / Object / Goal / 10 | — | The four ten-task suites most VLA papers report. Only Goal shares one scene across all its tasks. | 3 |
| LoRA | — | Low-rank adaptation. Fine-tuning that trains small added matrices instead of all the weights, which needs much less GPU memory. | 2 |
| MuJoCo | — | The physics engine LIBERO runs on. | 3 |
| openpi | — | Physical Intelligence's open-source code and checkpoints for π0, π0-FAST and π0.5. | 2 |
| patch | 图像块 | A small square of a picture. SigLIP cuts a 224×224 picture into 16×16 patches of 14 pixels, one token each. | 2 |
| PaliGemma | — | The vision-language model inside π0 and π0.5: a SigLIP image encoder plus the Gemma 2B language model. | 2 |
| policy | 策略 | A network that maps what the robot sees (and reads) to what it does. | 1 |
| reinforcement learning | 强化学习 | Learning by trying: the robot acts, gets a score, and is trained to do more of what scored well. π*0.6 uses it. | 2 |
| shortcut | 捷径 | A feature in the training data, such as the scene layout, that predicts the right action so well that the model never learns the intended one, such as reading the instruction. | 1, 4 |
| success rate | 成功率 | The share of episodes in which the simulator's goal condition was met. | 3 |
| transformer | — | The kind of network language models are built from; it works on a row of tokens, layer after layer, using attention. | 2 |
| VLA | 视觉-语言-动作模型 | Vision-language-action model: a policy built from a vision-language model that takes images and an instruction and outputs actions. | 1 |
| VLM | 视觉-语言模型 | Vision-language model: a model trained on images and text, such as PaliGemma. | 1 |
