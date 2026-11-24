import matplotlib.pyplot as plt

failure_times = [8, 20, 34, 46, 63, 86, 111, 141, 186, 266]

N = len(failure_times)

# Add starting time
times = [0] + failure_times

print("Time\tAlive\tInterval\tHazard\t\tDensity\t\tCDF\tReliability")

for i in range(N):
    start = times[i]
    end = times[i + 1]

    interval = end - start
    alive = N - i

    hazard = 1 / (alive * interval)
    density = 1 / (N * interval)

    cdf = (i + 1) / N
    reliability = 1 - cdf

    print(
        f"{end}\t{alive}\t{interval}\t\t"
        f"{hazard:.5f}\t\t{density:.5f}\t\t"
        f"{cdf:.2f}\t{reliability:.2f}"
    )

hazards = []
densities = []
cdfs = []
reliabilities = []
plot_times = []

for i in range(N):
    start = times[i]
    end = times[i + 1]

    interval = end - start
    alive = N - i

    hazard = 1 / (alive * interval)
    density = 1 / (N * interval)

    cdf = (i + 1) / N
    reliability = 1 - cdf

    plot_times.append(end)
    hazards.append(hazard)
    densities.append(density)
    cdfs.append(cdf)
    reliabilities.append(reliability)


plt.figure()
plt.plot(plot_times, hazards, marker="o")
plt.xlabel("Time (hours)")
plt.ylabel("Hazard z(t)")
plt.title("Hazard Function")
plt.grid()
plt.show()


plt.figure()
plt.plot(plot_times, densities, marker="o")
plt.xlabel("Time (hours)")
plt.ylabel("Density f(t)")
plt.title("Density Function")
plt.grid()
plt.show()


plt.figure()
plt.step(plot_times, cdfs, where="post")
plt.xlabel("Time (hours)")
plt.ylabel("F(t)")
plt.title("Cumulative Distribution Function")
plt.grid()
plt.show()


plt.figure()
plt.step(plot_times, reliabilities, where="post")
plt.xlabel("Time (hours)")
plt.ylabel("R(t)")
plt.title("Reliability Function")
plt.grid()
plt.show()
