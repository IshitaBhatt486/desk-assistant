import re

from robot import Robot


COMMAND_PATTERN = re.compile(
    r"^robot\.(\w+)\((.*?)\)$"
)


def parse_arguments(argument_string):
    argument_string = argument_string.strip()

    if not argument_string:
        return []

    parts = [
        part.strip()
        for part in argument_string.split(",")
    ]

    arguments = []

    for part in parts:
        try:
            arguments.append(float(part))
        except ValueError:
            raise ValueError(
                f"Invalid numeric argument: {part}"
            )

    return arguments


def execute_command(robot, command):
    command = command.strip()

    if command in {"quit()", "exit()"}:
        return False

    if command == "help":
        print()
        print("Commands:")
        print("  robot.forward(30, 25)")
        print("  robot.backward(20, 25)")
        print("  robot.turn(90, 20)")
        print("  robot.left(90, 20)")
        print("  robot.right(90, 20)")
        print("  robot.stop()")
        print("  robot.position()")
        print("  robot.reset_odometry()")
        print("  quit()")
        print()
        return True

    match = COMMAND_PATTERN.match(command)

    if not match:
        print(
            "Invalid command. Type 'help' for commands."
        )
        return True

    method_name = match.group(1)
    argument_string = match.group(2)

    try:
        args = parse_arguments(argument_string)
    except ValueError as e:
        print(e)
        return True

    allowed_methods = {
        "forward",
        "backward",
        "turn",
        "left",
        "right",
        "stop",
        "position",
        "reset_odometry",
    }

    if method_name not in allowed_methods:
        print(f"Unknown robot method: {method_name}")
        return True

    method = getattr(robot, method_name)

    try:
        result = method(*args)

        if result is not None:
            print(result)

    except TypeError as e:
        print(f"Invalid arguments: {e}")

    except RuntimeError as e:
        print(f"Robot error: {e}")

    return True


def main():
    robot = Robot()

    print("======================================")
    print("          DESK ROBOT TERMINAL")
    print("======================================")

    print("\nType 'help' for commands.")
    print("Type 'quit()' to exit.\n")

    try:
        while True:
            try:
                command = input(">>> ")

                if not execute_command(
                    robot,
                    command
                ):
                    break

            except KeyboardInterrupt:
                print("\nStopping robot...")
                robot.stop()
                break

            except EOFError:
                break

    finally:
        robot.close()


if __name__ == "__main__":
    main()