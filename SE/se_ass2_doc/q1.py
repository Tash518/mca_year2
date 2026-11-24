import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def constant_hazard(time, lam):
    return np.exp(-lam * time)


def linear_hazar(time, k):
    return np.exp(-(k * time**2) / 2)


def weibull_hazard(time, k, m):
    return np.exp(-(k * time ** (m + 1)) / (m + 1))


lam = 0.3
m = 0.5
k = 0.9

time = np.arange(1, 11)

print(time)

R1 = constant_hazard(time, lam)
R2 = linear_hazar(time, k)
R3 = weibull_hazard(time, k, m)
print(R1)
print(R2)
print(R3)

print("RELIABILITY RESULTS")
print("-" * 40)

print("CASE I")
print("Reliability at t = 3 hours:", constant_hazard(3, lam))

print()

print("CASE II")
print("Reliability at t = 5 hours:", linear_hazar(5, k))

print()

print("CASE III")
print("Reliability at t = 5 hours:", weibull_hazard(5, k, m))

df = pd.DataFrame(
    {
        "Time h": time,
        "CASE I": R1,
        "CASE I": R2,
        "CASE I": R3,
    }
)

print(df)

plt.plot(
    time,
    R1,
    marker="o",
    label = "CASE I - constant hazard"
)

plt.plot(
    time,
    R2,
    marker="o",
    label = "CASE II - linear hazard"
)

plt.plot(
    time,
    R3,
    marker="o",
    label = "CASE III - weibull hazard"
)

plt.xlabel("Time to Failure (hours)")
plt.ylabel("Reliability R(t)")

plt.title("Reliability vs Time to Failure")

plt.legend()

plt.show()