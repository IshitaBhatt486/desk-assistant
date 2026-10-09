from robot import Robot


def main():
    robot = Robot()

    print("Desk Assistant Robot")
    print("Commands:")
    print("  forward <speed>")
    print("  backward <speed>")
    print("  left <speed>")
    print("  right <speed>")
    print("  stop")
    print("  quit")

    try:
        while True:
            command = input("> ").strip()

            if not command:
                continue

            parts = command.split()
            action = parts[0].lower()

            if action == "quit":
                robot.stop()
                break

            if action == "stop":
                robot.stop()
                print("Stopped")
                continue

            if action not in {"forward", "backward", "left", "right"}:
                print("Unknown command")
                continue

            speed = float(parts[1]) if len(parts) > 1 else 30

            getattr(robot, action)(speed)

            print(f"{action} at {speed}%")

    except KeyboardInterrupt:
        print("\nStopping robot...")
        robot.stop()

    finally:
        robot.stop()


if __name__ == "__main__":
    main()