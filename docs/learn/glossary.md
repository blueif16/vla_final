# Glossary

Each term links to the chapter that explains it.

| Term | Meaning | Chapter |
|---|---|---|
| action | The numbers a policy outputs to move the robot. In LIBERO, seven: three for moving the hand, three for rotating it, one for the gripper. | 1 |
| action chunk | Several future actions predicted in one call. `pi05_libero` predicts 10, and the evaluation script runs 5 before asking again. | 1 |
| action expert | The smaller network in π0 and π0.5 that turns noise into an action chunk while attending to the VLM's output. | 2 |
| behaviour cloning | Training a policy to copy what a human operator did in recorded demonstrations. | 1 |
| CAG | Counterfactual Action Guidance, from the LIBERO-CF paper. Runs the policy with and without the instruction and amplifies the difference. | 5 |
| checkpoint | A saved set of trained model weights, such as `pi05_libero`. | 2 |
| counterfactual instruction | A feasible instruction for a different task in a scene the model already knows. | 4, 5 |
| episode (trial) | One run of the robot from a starting arrangement until success or the step limit. | 3 |
| faithful / biased success | Under a different-task instruction, whether the robot completed the new task (faithful) or the scene's original task (biased). | 4 |
| fine-tuning | Further training of a pretrained model on the tasks it will be tested on. | 1 |
| flow matching | A way to generate continuous outputs by learning to move random noise, step by step, towards real data. π0 and π0.5 use it for actions. | 1, 2 |
| grounding (language grounding) | Our working definition: changing the words changes what the robot does, in the way the words say. | 4 |
| grounding rate | How often the gripper touches the object the instruction names, whether or not the task finishes. | 4 |
| knowledge insulation | Stopping the action expert's training gradients from flowing into the VLM, so robot training doesn't erase the VLM's web knowledge. | 2 |
| LIBERO | A simulated benchmark of 130 manipulation tasks on a Franka Panda arm in MuJoCo. | 3 |
| LIBERO-Spatial / Object / Goal / 10 | The four ten-task suites most VLA papers report. Only Goal shares one scene across all its tasks. | 3 |
| LoRA | Low-rank adaptation. Fine-tuning that trains small added matrices instead of all the weights, which needs much less GPU memory. | 2 |
| MuJoCo | The physics engine LIBERO runs on. | 3 |
| openpi | Physical Intelligence's open-source code and checkpoints for π0, π0-FAST and π0.5. | 2 |
| PaliGemma | The vision-language model inside π0 and π0.5: a SigLIP image encoder plus the Gemma 2B language model. | 2 |
| policy | A network that maps what the robot sees (and reads) to what it does. | 1 |
| shortcut | A feature in the training data, such as the scene layout, that predicts the right action so well that the model never learns the intended one, such as reading the instruction. | 1, 4 |
| success rate | The share of episodes in which the simulator's goal condition was met. | 3 |
| VLA | Vision-language-action model: a policy built from a vision-language model that takes images and an instruction and outputs actions. | 1 |
| VLM | Vision-language model: a model trained on images and text, such as PaliGemma. | 1 |
