import math


def classify_project(kloc):
    if kloc <= 50:
        return "Organic", 0
    elif kloc <= 300:
        return "Semi-Detached", 1
    else:
        return "Embedded", 2


def basic_cocomo(loc):
    kloc = loc / 1000.0
    proj_type, idx = classify_project(kloc)

    #[organic, semi detached, embedded]
    a_b = [2.4, 3.0, 3.6]
    b_b = [1.05, 1.12, 1.20]
    c_b = [2.5, 2.5, 2.5]
    d_b = [0.38, 0.35, 0.32]

    effort = a_b[idx] * (kloc ** b_b[idx])
    dev_time = c_b[idx] * (effort ** d_b[idx])
    staff = effort / dev_time if dev_time > 0 else 0

    print("\n" + "=" * 45)
    print("         BASIC COCOMO I RESULTS")
    print("=" * 45)
    print(f"Lines of Code (LOC)    : {loc:,} ({kloc:.2f} KLOC)")
    print(f"Project Type           : {proj_type}")
    print(f"Estimated Effort (E)   : {effort:.2f} Person-Months")
    print(f"Development Time (D)   : {dev_time:.2f} Months")
    print(f"People Engaged (P)     : {math.ceil(staff)} Persons ({staff:.2f} avg)")
    print("=" * 45)


def intermediate_cocomo(loc, cost_drivers):
    kloc = loc / 1000.0
    proj_type, idx = classify_project(kloc)

    #[organic, semi detached, embedded]
    a_i = [3.2, 3.0, 2.8]
    b_i = [1.05, 1.12, 1.20]
    c_i = [2.5, 2.5, 2.5]
    d_i = [0.38, 0.35, 0.32]

    #(EAF)
    eaf = 1.0
    for val in cost_drivers:
        if val is not None and val > 0:
            eaf *= val

    effort = a_i[idx] * (kloc ** b_i[idx]) * eaf
    dev_time = c_i[idx] * (effort ** d_i[idx])
    staff = effort / dev_time if dev_time > 0 else 0

    print("\n" + "=" * 45)
    print("      INTERMEDIATE COCOMO I RESULTS")
    print("=" * 45)
    print(f"Lines of Code (LOC)    : {loc:,} ({kloc:.2f} KLOC)")
    print(f"Project Type           : {proj_type}")
    print(f"EAF Value              : {eaf:.4f}")
    print(f"Estimated Effort (E)   : {effort:.2f} Person-Months")
    print(f"Development Time (D)   : {dev_time:.2f} Months")
    print(f"People Engaged (P)     : {math.ceil(staff)} Persons ({staff:.2f} avg)")
    print("=" * 45)


def get_cost_drivers():
    default_drivers = [
        1.15,  #RELY
        1.30,  #DATA
        1.10,  #CPLX
        1.16,  #TIME
        1.40,  #STOR
        0.85,  #VIRT
        0.70,  #TURN
        1.21,  #ACAP
        0.86,  #AEXP
        0.90,  #PCAP
        1.00,  #VEXP
        1.00,  #LEXP
        0.80,  #MODP
        1.00,  #TOOL
        0.83,  #SCED
    ]

    print("predefined values from the Example Table")

    print("Loaded 15 predefined Cost Drivers:", default_drivers)
    return default_drivers


def main():
    while True:
        print("COCOMO I MENU")
        print("1. Basic COCOMO Model")
        print("2. Intermediate COCOMO Model")
        print("3. Exit")
        print("===============================================")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "3":
            print("Exiting program.")
            break

        if choice in ("1", "2"):
            try:
                loc = float(input("Enter total Lines of Code (LOC): "))
                if loc <= 0:
                    print("LOC must be greater than 0.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid number for LOC.")
                continue

            if choice == "1":
                basic_cocomo(loc)
            elif choice == "2":
                drivers = get_cost_drivers()
                intermediate_cocomo(loc, drivers)
        else:
            print("Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()