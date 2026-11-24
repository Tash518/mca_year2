def calculate_object_points(screens, reports, components):
    op = (screens * 2) + (reports * 5) + (components * 10)
    return op

def calculate_nop(op, reuse_percentage):
    nop = op * (1 - (reuse_percentage / 100.0))
    return nop

def calculate_effort(nop, prod_rate=13):
    effort = nop / prod_rate
    return effort

def calculate_people(effort, duration_years):
    duration_months = duration_years * 12
    people = effort / duration_months
    return people

def main():
    screens = 10
    reports = 4
    components = 15
    reuse_percentage = 60.0
    duration_years = 5.0
    op = calculate_object_points(screens, reports, components)
    nop = calculate_nop(op, reuse_percentage)
    effort = calculate_effort(nop)
    people = calculate_people(effort, duration_years)

    while True:
        print("\n" + "="*45)
        print("     COCOMO II - MENU DRIVEN PROGRAM")
        print("="*45)
        print("1. Determine Object Points (OP)")
        print("2. Determine New Object Points (NOP)")
        print("3. Determine Effort (Person-Months)")
        print("4. Determine Number of People Engaged (5-Year Duration)")
        print("5. Run All & Show Full Report")
        print("6. Exit")
        print("="*45)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            print(f"\n[Result] Total Object Points (OP): {op}")
        elif choice == '2':
            print(f"\n[Result] New Object Points (NOP) with {reuse_percentage}% reuse: {nop:.2f}")
        elif choice == '3':
            print(f"\n[Result] Estimated Effort: {effort:.2f} Person-Months")
        elif choice == '4':
            print(f"\n[Result] Number of People Required ({duration_years} years duration): {people:.2f} (approx. {round(people)} person/people)")
        elif choice == '5':
            print("\n--- FULL CALCULATION REPORT ---")
            print(f"• Inputs: {screens} Screens, {reports} Reports, {components} 3GL Components, {reuse_percentage}% Reuse")
            print(f"• 1. Object Points (OP): {op}")
            print(f"• 2. New Object Points (NOP): {nop:.2f}")
            print(f"• 3. Effort Required: {effort:.2f} Person-Months")
            print(f"• 4. Team Size Required: {people:.2f} People ({duration_years} years / {duration_years * 12} months)")
        elif choice == '6':
            print("\nExiting program. Goodbye!")
            break
        else:
            print("\nInvalid choice! Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()