import matplotlib.pyplot as plt


# ==================================================
# ADAPTIVE FLOW - FINAL EXPERIMENTAL RESULTS
# ==================================================

controllers = [
    "Fixed-Time",
    "Rule-Based",
    "Q-Learning",
    "DQN"
]

average_queue = [
    194.07,
    193.99,
    90.91,
    86.63
]

average_waiting_time = [
    50.26,
    50.23,
    25.70,
    23.44
]

throughput = [
    788,
    788,
    368,
    386
]

max_waiting_time = [
    78,
    75,
    73,
    54
]


# ==================================================
# GRAPH 1 - AVERAGE QUEUE LENGTH
# ==================================================

plt.figure(figsize=(10, 6))

plt.bar(
    controllers,
    average_queue,
    color="purple"
)

plt.title(
    "Adaptive Flow - Average Queue Length"
)

plt.xlabel(
    "Controller"
)

plt.ylabel(
    "Average Queue Length"
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

plt.savefig(
    "average_queue.png",
    dpi=300
)

plt.show()


# ==================================================
# GRAPH 2 - AVERAGE WAITING TIME
# ==================================================

plt.figure(figsize=(10, 6))

plt.plot(
    controllers,
    average_waiting_time,
    marker="o",
    color="pink",
)

plt.title(
    "Adaptive Flow - Average Waiting Time"
)

plt.xlabel(
    "Controller"
)

plt.ylabel(
    "Average Waiting Time"
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

plt.savefig(
    "average_waiting_time.png",
    dpi=300
)

plt.show()


# ==================================================
# GRAPH 3 - THROUGHPUT
# ==================================================

plt.figure(figsize=(10, 6))

plt.bar(
    controllers,
    throughput
)

plt.title(
    "Adaptive Flow - Throughput Comparison"
)

plt.xlabel(
    "Controller"
)

plt.ylabel(
    "Vehicles Passed"
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

plt.savefig(
    "throughput.png",
    dpi=300
)

plt.show()


# ==================================================
# GRAPH 4 - MAXIMUM WAITING TIME
# ==================================================

plt.figure(figsize=(10, 6))

plt.plot(
    controllers,
    max_waiting_time,
    marker="o"
)

plt.title(
    "Adaptive Flow - Maximum Waiting Time"
)

plt.xlabel(
    "Controller"
)

plt.ylabel(
    "Maximum Waiting Time"
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

plt.savefig(
    "maximum_waiting_time.png",
    dpi=300
)

plt.show()


print("\n==============================================")
print("🚦 ADAPTIVE FLOW - GRAPHS CREATED")
print("==============================================")

print("✅ average_queue.png")
print("✅ average_waiting_time.png")
print("✅ throughput.png")
print("✅ maximum_waiting_time.png")

print("\n🎉 All graphs generated successfully!")