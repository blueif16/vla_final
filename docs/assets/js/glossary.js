/* Side notes for every term the chapters use. One entry per term; t = name, zh = the Chinese term people use
   (concepts only; names such as LIBERO or PaliGemma get none), d = plain definition, more = optional pointer.
   Shared by all chapters, so a term is defined once for the whole site. The Chinese terms were checked against
   Chinese technical writing on 2026-11-11 (library/terms-zh.yaml).
   Sources for the facts are in library/papers.yaml. */
window.GLOSSARY = {
  "neural-network": { t: "neural network", zh: "神经网络", d: "A program made of millions or billions of adjustable numbers that learns a task from examples instead of following rules someone wrote by hand." },
  "parameters": { t: "parameters", zh: "参数", d: "The adjustable numbers inside a neural network. Training sets their values. Their count is the usual way to say how big a model is, so a 7-billion-parameter model has 7 billion of them." },
  "vla": { t: "VLA · vision-language-action model", zh: "视觉-语言-动作模型", d: "A neural network that takes camera images and a written instruction and outputs robot actions. It is made by taking a vision-language model and training it further on robot demonstrations.", more: "Chapter 1" },
  "vlm": { t: "VLM · vision-language model", zh: "视觉-语言模型", d: "A neural network trained on images paired with text from the web, so it can describe a picture or answer questions about it. PaliGemma is one." },
  "policy": { t: "policy", zh: "策略", d: "The robotics word for whatever decides a robot's next action from what it senses right now. A VLA is one kind of policy." },
  "action": { t: "action", zh: "动作", d: "The numbers sent to the robot for one time step. In LIBERO an action is seven numbers: three move the hand, three turn it and one opens or closes the gripper." },
  "action-chunk": { t: "action chunk", zh: "动作块", d: "Several future actions predicted in one call. π0 predicts 50; the LIBERO version of π0.5 predicts 10, and the evaluation script runs the first 5 before asking again." },
  "libero": { t: "LIBERO", d: "A benchmark of 130 robot manipulation tasks in simulation, with a simulated Franka Panda arm. Our project tests models on four of its ten-task suites.", more: "Chapter 3" },
  "benchmark": { t: "benchmark", zh: "基准测试", d: "A fixed set of tasks with a fixed scoring rule, so different models can be compared on equal terms." },
  "simulator": { t: "simulator", zh: "仿真器", d: "Software that computes how a robot and the objects around it would move under real physics, so experiments can run on a computer instead of a real robot." },
  "mujoco": { t: "MuJoCo", d: "A physics engine for simulating robots and contact between objects. LIBERO runs on it, through a library called robosuite." },
  "franka": { t: "Franka Panda", d: "A seven-joint robot arm made by Franka Robotics in Germany, common in research labs. LIBERO simulates this arm." },
  "teleoperation": { t: "teleoperation", zh: "遥操作", d: "A person steering a robot by hand from a distance, often by moving a matching 'leader' arm that the robot copies. The recorded runs become training data." },
  "demonstration": { t: "demonstration", zh: "演示", d: "One recorded run of a task done by a person through teleoperation: the camera images, the instruction and the action at every time step." },
  "paligemma": { t: "PaliGemma", d: "A vision-language model from Google with about 3 billion parameters. It joins the SigLIP image encoder to the Gemma language model. π0 and π0.5 are built on it." },
  "siglip": { t: "SigLIP", d: "An image encoder from Google. It turns a picture into a list of number vectors that a language model can read like words." },
  "gemma": { t: "Gemma", d: "A family of open language models from Google. π0 and π0.5 use the 2-billion-parameter version inside PaliGemma." },
  "llama2": { t: "Llama 2", d: "An open language model from Meta, released in 2023. OpenVLA is built on its 7-billion-parameter version." },
  "deepmind": { t: "Google DeepMind", d: "Google's AI research lab. It built RT-2." },
  "rt2": { t: "RT-2", d: "Robotics Transformer 2, from Google DeepMind (2023). It wrote robot actions as text tokens and showed that what a model learned from the web carries over to robot control." },
  "openvla": { t: "OpenVLA", d: "An open VLA with 7 billion parameters (2024), built on Llama 2 and trained on 970,000 robot episodes from Open X-Embodiment. It writes actions as tokens." },
  "physical-intelligence": { t: "Physical Intelligence", d: "A robotics AI company in San Francisco. It makes the π models and releases some of them, with code, as openpi." },
  "pi0": { t: "π0 · pi-zero", d: "Physical Intelligence's first VLA (2024). PaliGemma plus a flow-matching action expert that predicts 50-step action chunks.", more: "Chapter 2" },
  "pi05": { t: "π0.5", d: "Physical Intelligence's 2025 successor to π0, trained on more varied data so it can work in homes it has never seen. Its LIBERO version is the model in our project.", more: "Chapter 2" },
  "openpi": { t: "openpi", d: "Physical Intelligence's open-source code for π0 and π0.5, with trained checkpoints. It includes the LIBERO version of π0.5 and the script that evaluates it.", more: "Chapter 2" },
  "token": { t: "token", zh: "词元", d: "The unit a language model reads and writes: a word, part of a word or a number. The model writes its output one token at a time, each one depending on the ones before." },
  "action-expert": { t: "action expert", zh: "动作专家", d: "A smaller network that sits next to the VLM in π0 and π0.5 (about 300 million parameters). It can read everything the VLM computed and turns random noise into an action chunk.", more: "Chapter 2" },
  "diffusion": { t: "diffusion", zh: "扩散模型", d: "A way to generate data by starting from random noise and removing the noise step by step. Image generators use it, and diffusion policies use it to generate robot motions." },
  "flow-matching": { t: "flow matching", zh: "流匹配", d: "A close relative of diffusion. The model learns, for any partly noisy guess, which direction leads towards real data, and follows that direction for a few steps. π0 and π0.5 generate actions this way." },
  "behaviour-cloning": { t: "behaviour cloning", zh: "行为克隆", d: "Learning by imitation. The model sees what the robot saw and is trained to output what the human operator did at that moment." },
  "pretraining": { t: "pretraining", zh: "预训练", d: "The early stages of training on large, broad data, meant to give a model general knowledge before it sees the tasks it will be tested on." },
  "fine-tuning": { t: "fine-tuning", zh: "微调", d: "Further training of a pretrained model on the specific robot and tasks it will be tested on, usually with much less data." },
  "oxe": { t: "Open X-Embodiment", d: "A robot dataset pooled from many labs in 2023: more than a million recorded episodes from 22 kinds of robot." },
  "fast": { t: "FAST", d: "An action tokenizer from Physical Intelligence (2025). It compresses an action chunk with a discrete cosine transform, the maths behind JPEG, before turning it into tokens, so far fewer tokens are needed." },
  "joint-readings": { t: "joint readings", zh: "关节状态", d: "The angles the robot's motors report about themselves, also called the robot's state or proprioception." },
  "episode": { t: "episode", zh: "回合", d: "One attempt at a task, from the starting arrangement until success or until the step limit runs out." }
};
