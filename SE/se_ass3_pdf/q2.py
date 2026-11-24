import math


def application_composition():
    print("APPLICATION COMPOSITION MODEL")
    print("1. Use problem preset ")
    print("2. Enter custom values")
    mode = input("Select option (1 or 2): ").strip()

    #[simple, average, complex]
    weights = {
        "Screens": [1, 2, 3],
        "Reports": [2, 5, 8],
        "Components": [1, 1, 10],
    }

    if mode == "1":
        counts = {"Screens": 14, "Reports": 6, "Components": 10}
        reuse_pct = 90.0
        productivity = 25.0
        labour_rate = 1500.0
        print("\nSelect Complexity Level for Preset Counts:")
        print("1. Simple   2. Average (Default)   3. Complex")
        c_choice = input("Enter choice (1-3): ").strip()
        c_idx = 0 if c_choice == "1" else (2 if c_choice == "3" else 1)
    else:
        counts = {
            "Screens": int(input("Enter number of Screens: ")),
            "Reports": int(input("Enter number of Reports: ")),
            "Components": int(input("Enter number of 3GL Components: ")),
        }
        print("\nSelect Complexity Level:")
        print("1. Simple   2. Average   3. Complex")
        c_choice = input("Enter choice (1-3): ").strip()
        c_idx = 0 if c_choice == "1" else (2 if c_choice == "3" else 1)

        reuse_pct = float(input("Enter % Reuse (0 - 100): "))
        productivity = float(input("Enter Productivity Rate (PROD): "))
        labour_rate = float(input("Enter Labour Rate ($ per Person-Month): "))

    complexity_names = ["Simple", "Average", "Complex"]

    # object points
    op_screens = counts["Screens"] * weights["Screens"][c_idx]
    op_reports = counts["Reports"] * weights["Reports"][c_idx]
    op_components = counts["Components"] * weights["Components"][c_idx]
    total_op = op_screens + op_reports + op_components

    # new object points
    nop = total_op * ((100.0 - reuse_pct) / 100.0)

    # effor (Person-Months) & total cost
    effort = nop / productivity if productivity > 0 else 0
    total_cost = effort * labour_rate

    print("\n" + "=" * 52)
    print("      APPLICATION COMPOSITION MODEL RESULTS")
    print("=" * 52)
    print(f"Complexity Level Applied : {complexity_names[c_idx]}")
    print(f"Object Points (OP)       : {total_op:.2f}")
    print(f"New Object Points (NOP)  : {nop:.2f}")
    print(f"Estimated Effort (E)     : {effort:.4f} Person-Months")
    print(f"Total Project Cost       : ${total_cost:,.2f} (@ ${labour_rate:,.0f}/PM)")
    print("=" * 52)


def get_scale_exponent():
    print("\nScale Exponent (B) Input:")
    print("1. Use Nominal Scale Factors (Sum = 18.97 -> B = 1.10)")
    print("2. Enter 5 Scale Factors (PREC, FLEX, RESL, TEAM, PMAT)")
    choice = input("Select option (1 or 2): ").strip()
    if choice == "2":
        sf_names = ["PREC", "FLEX", "RESL", "TEAM", "PMAT"]
        sf_sum = sum(float(input(f"  Enter {name}: ")) for name in sf_names)
        return 0.91 + 0.01 * sf_sum
    return 1.10


def get_effort_multipliers(count, label):
    print(f"\n{label} ({count} Effort Multipliers):")
    print("1. Use Nominal Multipliers (All = 1.0, Product EAF = 1.0)")
    print(f"2. Enter {count} Custom Effort Multiplier values")
    choice = input("Select option (1 or 2): ").strip()
    if choice == "2":
        eaf = 1.0
        for i in range(1, count + 1):
            val = float(input(f"  EM{i}: "))
            if val > 0:
                eaf *= val
        return eaf
    return 1.0


def early_design_model():
    print("EARLY DESIGN STAGE MODE")
    size_kloc = float(input("Enter Estimated Software Size (in KSLOC): "))
    years = float(input("Enter Development Duration in Years (default 5): ") or 5.0)

    a = 2.94
    b = get_scale_exponent()
    eaf = get_effort_multipliers(7, "Early Design")

    effort = a * (size_kloc ** b) * eaf
    months = years * 12.0
    staff = effort / months if months > 0 else 0

    print("\n" + "=" * 52)
    print("         EARLY DESIGN STAGE MODEL RESULTS")
    print("=" * 52)
    print(f"Software Size            : {size_kloc:.2f} KSLOC")
    print(f"Scale Exponent (B)       : {b:.4f}")
    print(f"Effort Multiplier (EAF)  : {eaf:.4f}")
    print(f"Estimated Effort (E)     : {effort:.2f} Person-Months")
    print(f"Duration                 : {years:.1f} Years ({months:.0f} Months)")
    print(f"People Engaged (P)       : {math.ceil(staff)} Persons ({staff:.2f} avg)")
    print("=" * 52)


def post_architecture_model():
    print("POST-ARCHITECTURE STAGE MODEL")
    size_kloc = float(input("Enter Estimated Software Size (in KSLOC): "))
    years = float(input("Enter Development Duration in Years (default 5): ") or 5.0)

    a = 2.94
    b = get_scale_exponent()
    eaf = get_effort_multipliers(17, "Post-Architecture")

    effort = a * (size_kloc ** b) * eaf
    months = years * 12.0
    staff = effort / months if months > 0 else 0

    print("\n" + "=" * 52)
    print("       POST-ARCHITECTURE STAGE MODEL RESULTS")
    print("=" * 52)
    print(f"Software Size            : {size_kloc:.2f} KSLOC")
    print(f"Scale Exponent (B)       : {b:.4f}")
    print(f"Effort Multiplier (EAF)  : {eaf:.4f}")
    print(f"Estimated Effort (E)     : {effort:.2f} Person-Months")
    print(f"Duration                 : {years:.1f} Years ({months:.0f} Months)")
    print(f"People Engaged (P)       : {math.ceil(staff)} Persons ({staff:.2f} avg)")
    print("=" * 52)


def main():
    while True:
        print("COCOMO II MENU")
        print("1. Application Composition Model")
        print("2. Early Design Stage Model")
        print("3. Post-Architecture Stage Model")
        print("4. Exit")
        print("==================================================")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            application_composition()
        elif choice == "2":
            early_design_model()
        elif choice == "3":
            post_architecture_model()
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select 1 to 4.")


if __name__ == "__main__":
    main()