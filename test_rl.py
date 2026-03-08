"""Quick smoke test for the RL engine."""
from rl_engine import (
    compute_generalized_cost, rank_modes,
    MaaSEnvironment, DQNAgent,
    GIUSEPPE, MODES, RL_CONFIG,
)

print("=== RL ENGINE IMPORT TEST ===")
print("Modes:", MODES)
print("User:", GIUSEPPE.name, "age="+str(GIUSEPPE.age), "segment="+GIUSEPPE.segment)
print()

print("=== GENERALIZED COST TEST ===")
for mode in MODES:
    gc = compute_generalized_cost(mode, GIUSEPPE)
    print("  %-20s GC=%6.2f  raw=%6.2f" % (mode, gc["gc_total"], gc["gc_raw"]))
print()

print("=== RANKED MODES (Phase 0) ===")
ranked = rank_modes(GIUSEPPE, current_phase=0)
for i, r in enumerate(ranked):
    print("  %d. %-20s GC=%6.2f" % (i+1, r["mode"], r["gc_total"]))
print()

print("=== ENVIRONMENT TEST ===")
env = MaaSEnvironment(user=GIUSEPPE, num_weeks=2, seed=42)
state = env.reset()
print("State dim:", len(state), "expected:", RL_CONFIG.state_dim)
print("Num actions:", env.num_actions)
action = 10
next_state, reward, done, info = env.step(action)
print("Step result: reward=%.3f, done=%s, mode=%s" % (reward, done, info["actual_mode"]))
print()

print("=== DQN AGENT TEST ===")
agent = DQNAgent(RL_CONFIG)
action = agent.select_action(state, training=True)
print("Agent selected action:", action)
q_vals = agent.get_q_values(state)
print("Q-values shape:", q_vals.shape, "range=[%.4f, %.4f]" % (q_vals.min(), q_vals.max()))
print()

print("=== MINI TRAINING TEST (10 episodes) ===")
from rl_engine import train
result = train(num_episodes=10, num_weeks=2, seed=42, verbose=False)
hist = result["history"]
print("Episodes trained:", len(hist["episode_rewards"]))
print("Last reward: %.2f" % hist["episode_rewards"][-1])
print("Last green ratio: %.1f%%" % (hist["episode_green_ratios"][-1]*100))
print("Last CO2 saved: %.1f kg" % hist["episode_co2_saved"][-1])
summary = result["env"].get_summary()
print("Final phase:", summary["final_phase"])
print("Final habit:", summary["final_habit"])
print()
print("ALL TESTS PASSED")
