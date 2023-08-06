from terminalpackagehamderber import terminal_settings as settings, command_handler


def start():
    command_handler.run_command("Clrscrn")
    settings.apply_settings()


def run_terminal_loop():
    start()
    while True:
        # Main program loop. Constantly tries to get commands from the user, displaying the username
        # Ex: command line showing 'admin>'
        command_handler.get_user_input(f"admin> ")


if __name__ == "__main__":
    # Runs main but only if IDE 'run' is performed from this file
    run_terminal_loop()
