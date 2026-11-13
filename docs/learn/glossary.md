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
| reinforcement learning (RL) | 强化学习 | Learning by trying: the robot acts, gets a score, and is trained to do more of what scored well. π*0.6 uses it. | 2, RL 1 |
| shortcut | 捷径 | A feature in the training data, such as the scene layout, that predicts the right action so well that the model never learns the intended one, such as reading the instruction. | 1, 4 |
| success rate | 成功率 | The share of episodes in which the simulator's goal condition was met. | 3 |
| transformer | — | The kind of network language models are built from; it works on a row of tokens, layer after layer, using attention. | 2 |
| VLA | 视觉-语言-动作模型 | Vision-language-action model: a policy built from a vision-language model that takes images and an instruction and outputs actions. | 1 |
| VLM | 视觉-语言模型 | Vision-language model: a model trained on images and text, such as PaliGemma. | 1 |

## Reinforcement learning series

Terms from the RL chapters (`rl-*.md`). The Chinese choices and their alternatives are under `rl:` in
`library/terms-zh.yaml`.

| Term | 中文 | Meaning | Chapter |
|---|---|---|---|
| actor-critic | 演员-评论员 | A player (the policy) plus a coach that learns how good each situation is and says after every move whether things went better or worse than expected. | RL 3 |
| advantage | 优势 | How much better than usual a try or an action went: its score minus the average, or minus what the coach expected. | RL 1, RL 3, RL 7 |
| agent | 智能体 | The learner in RL: the thing that acts and is scored. | RL 1 |
| agentic RL | | RL where the model works through a whole task in many steps in a sandbox (terminal, browser, code) and is graded at the end. | RL 4, RL 5 |
| bandit | 多臂赌博机 | An RL problem with one choice, an instant reward and nothing afterwards that depends on it, such as which headline to show. | RL 3 |
| credit assignment | 信用分配 | Working out which of many actions earned a score that came only at the end. | RL 2 |
| discount | | A factor (such as 0.99 per step) that makes a reward count for less the later it comes after an action. | RL 2, RL 3 |
| DPO | — | Direct preference optimisation. Trains on pairs of answers where one was preferred, with no separate reward model and no sampling during training. RL-flavoured, not RL. | RL 4 |
| environment | 环境 | The world the agent acts in. In today's industry sense, a task plus a sandbox to act in plus a grader. | RL 1, RL 5 |
| exploration vs exploitation | 探索与利用 | The trade-off between trying something new and using what already works. | RL 2 |
| GRPO | — | Group relative policy optimisation. Samples a group of answers to one question and pushes each up or down by how it compares with the group's average. No coach network. | RL 4, RL 5 |
| model-based RL | 基于模型的强化学习 | RL that learns how the world responds to actions and plans by imagining moves ahead. MuZero. | RL 3 |
| offline RL | | RL from data already collected, without new tries during training. Recap works this way. | RL 7 |
| on-policy distillation | | The student model writes its own answers and a teacher grades every token of them. Used to merge RL-trained specialists into one model. | RL 5 |
| policy gradient | 策略梯度 | Learning the habits directly: make the actions from better-than-average tries more likely. REINFORCE is the basic version. | RL 1, RL 3 |
| PPO | — | Proximal policy optimisation. An actor-critic method with a limit on how much one update may change any action's chance. | RL 3, RL 4 |
| Q-learning | — | A value-based method that fills in a score sheet of how good each move is in each situation from experience. DQN does it with a neural network. | RL 3 |
| Recap | — | Physical Intelligence's method behind π*0.6: a value function labels each action "Advantage: positive" or "negative" as text, the policy is trained with the label, and it runs with "positive". | RL 7 |
| reward | 奖励 | The score the environment hands back to the agent. | RL 1 |
| reward hacking | 奖励黑客 | The agent raises its score in a way its designers didn't intend, such as circling for points instead of finishing a race. Also called specification gaming. | RL 2, RL 5 |
| reward model | 奖励模型 | A network trained on people's comparisons of answers to predict which one they'd prefer; it then scores answers during RLHF. | RL 4 |
| RLAIF / Constitutional AI | — | RL from AI feedback: an AI judge compares answers against a written list of principles. | RL 4 |
| RLHF | — | RL from human feedback: people compare answers, a reward model learns their taste, and the model is trained to score well with it. | RL 4 |
| RLVR | — | RL with verifiable rewards: the grade comes from a checker, such as an answer key or a test suite. | RL 4 |
| rubric reward | | A grade from an AI judge that scores an answer against a checklist written for that prompt; for tasks with no answer key. | RL 5 |
| value / value function | 价值函数 | A learned estimate of how good a situation (or a move in it) is: the score sheet, or the coach. | RL 3, RL 7 |
