Le-rebot

- Setup
    - git clone https://github.com/huggingface/lerobot.git
    - cd lerobot
    - python -m venv venv
    - source venv/bin/activate
    - pip install -e .

- Simulation
    - python lerobot/scripts/visualize_dataset.py \
    --repo-id lerobot/pusht \
    --episode-index 0

    - python lerobot/scripts/eval.py \
    -p lerobot/diffusion_pusht \
    eval.n_episodes=10 \
    eval.batch_size=10



- Reference
    - https://huggingface.co/lerobot/diffusion_pusht
    - https://github.com/huggingface/lerobot
    - https://github.com/AlexanderKoch-Koch/low_cost_robot
    - https://github.com/jess-moss/koch-v1-1
    - https://github.com/huggingface/lerobot/blob/main/examples/7_get_started_with_real_robot.md