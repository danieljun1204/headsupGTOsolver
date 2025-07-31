from src.cfr import CFRTrainer

if __name__ == "__main__":
    trainer = CFRTrainer()
    trainer.train(iterations=5000, log_every=500)

    print("\nFinal Strategy Profile:")
    profile = trainer.get_strategy_profile()
    for key, strategy in sorted(profile.items()):
        pretty = ', '.join(f"{a}: {strategy[a]:.2f}" for a in strategy)
        print(f"{key:<12} → {pretty}")
