import numpy as np
import matplotlib.pyplot as plt

time_intervals = np.array([0, 1000, 2000, 3000, 4000, 5000, 6000])

failures = np.array([59, 24, 29, 30, 17, 13])

N = np.sum(failures)
interval_width = np.diff(time_intervals)

density = failures / (N * interval_width)

cumulative_failures = np.cumsum(failures)
F_values = np.concatenate(([0], cumulative_failures / N))

R_values = 1 - F_values

hazard = density / R_values[:-1]


print("Total components:", N)

print("\nInterval-wise calculated values:")
print("-" * 95)

print(
    f"{'Interval':<15}{'Failures':<12}"
    f"{'f(t)':<15}{'F(t)':<15}"
    f"{'R(t)':<15}{'z(t)':<15}"
)

print("-" * 95)

for i in range(len(failures)):

    interval = f"{time_intervals[i]}-{time_intervals[i+1]}"

    print(
        f"{interval:<15}"
        f"{failures[i]:<12}"
        f"{density[i]:<15.8f}"
        f"{F_values[i+1]:<15.6f}"
        f"{R_values[i+1]:<15.6f}"
        f"{hazard[i]:<15.8f}"
    )


t_plot = []
f_plot = []
F_plot = []
R_plot = []
z_plot = []

for i in range(len(failures)):

    t = np.linspace(time_intervals[i], time_intervals[i + 1], 200, endpoint=False)

    F = F_values[i] + density[i] * (t - time_intervals[i])

    R = 1 - F

    f = np.full(len(t), density[i])

    z = f / R

    t_plot.extend(t)
    f_plot.extend(f)
    F_plot.extend(F)
    R_plot.extend(R)
    z_plot.extend(z)


plt.figure(figsize=(12, 9))

plt.subplot(2, 2, 1)
plt.plot(t_plot, z_plot, color="red")
plt.title("Hazard Function z(t)")
plt.xlabel("Time (hours)")
plt.ylabel("Hazard Rate")
plt.grid(True)

plt.subplot(2, 2, 2)
plt.stairs(density, time_intervals, color="blue")
plt.title("Density Function f(t)")
plt.xlabel("Time (hours)")
plt.ylabel("Probability Density")
plt.grid(True)

plt.subplot(2, 2, 3)
plt.plot(t_plot, F_plot, color="green")
plt.title("Cumulative Distribution Function F(t)")
plt.xlabel("Time (hours)")
plt.ylabel("Cumulative Probability")
plt.grid(True)

plt.subplot(2, 2, 4)
plt.plot(t_plot, R_plot, color="purple")
plt.title("Reliability Function R(t)")
plt.xlabel("Time (hours)")
plt.ylabel("Reliability")
plt.grid(True)


plt.tight_layout()
plt.show()
