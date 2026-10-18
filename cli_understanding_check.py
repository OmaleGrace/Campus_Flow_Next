
def run_cli_understanding_check():
    """
    Runs an interactive engineering quiz inside the CLI terminal window.
    Returns the total integer score achieved out of 3 points.
    """
    score = 0
    questions = [
        {
            "q": "Why should a ticket search function avoid modifying the master data layer collection directly?",
            "options": [
                "1. Because search operations are inherently read-only and mutating state causes data loss across menus.",
                "2. Because it speeds up terminal layout processing delays.",
                "3. Python loops throw syntax failures if lists are filtered."
            ],
            "correct": "1"
        },
        {
            "q": "When evaluation logic combines multiple simultaneous search parameters, which logic gate applies?",
            "options": [
                "1. OR logic rules",
                "2. AND logic rules (all constraints must match)",
                "3. XOR exclusion filtering"
            ],
            "correct": "2"
        },
        {
            "q": "Why is a ticket resting in a 'resolved' state strictly prohibited from receiving new follow-up notes?",
            "options": [
                "1. Resolved states mean closed contracts; changes bypass administrative compliance tracking without reopening.",
                "2. The JSON data loader framework cannot interpret notes appended onto resolved object keys.",
                "3. It saves terminal workspace memory layouts."
            ],
            "correct": "1"
        }
    ]
    
    print("\n=== CAMPUSFLOW NEXT: CLI ENGINEERING UNDERSTANDING CHECK ===")
    for index, item in enumerate(questions, 1):
        print(f"\nQuestion {index}: {item['q']}")
        for option in item["options"]:
            print(option)
            
        choice = input("Select answer (1-3): ").strip()
        if choice == item["correct"]:
            print("Correct Answer.")
            score += 1
        else:
            print(f" Incorrect. The ideal choice was Option {item['correct']}.")
            
    print(f"\n Evaluation Complete! You scored: {score} / {len(questions)} points.")
    
    percentatge = round(((score/len(questions))*100), 2)
    print(f"\nPercentage = {percentatge}")
    return score
