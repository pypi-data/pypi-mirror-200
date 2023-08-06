from enum import Enum
from terminalpackagehamderber.src import terminal_settings

import os


class CommandType(Enum):
    Single = 0,
    Multi = 1,
    Both = 2


class CommandObject:
    def __init__(self,
                 cmd_name='Unnamed command',
                 cmd_type=CommandType.Single,
                 cmd_help="Help undefined for 'COMMAND' at this time. Displaying the help page.",
                 cmd_func=None
                 ):
        self.cmd_name = cmd_name
        self.cmd_type = cmd_type
        self.cmd_help = cmd_help
        self.cmd_func = cmd_func

    def command(self, args=None):
        return self.cmd_func(args)

    def help(self):
        return str.replace(self.cmd_help, 'COMMAND', self.cmd_name)


def get_user_input(input_prompt="Default prompt: "):
    """
    Takes the user's input and drops it to lowercase and submits it to the command parser
    :param input_prompt:
    """
    user_input = str.lower(input(input_prompt))
    command_parser(user_input)


def run_command(text, args=None):
    try:
        command_dict[str.lower(text)].command(args)
    except KeyError:
        unknown_command()


def incomplete_multi_command():
    """
    Acknowledges that the multi-command was recognized, but that not enough information was submitted. Prompts
    the user to get help.
    """
    print(f"The command entered was recognized, but incomplete.")


def unknown_command():
    """
    Prints 'Unknown command' as well as the prompt for getting help.
    """
    print(f"Unknown command. Type 'help' for a list of commands.")


def help_command(args=None):
    """
    Help: Provides amplifying information on whatever is requested.
    :param args:
    """

    def print_all_help():
        """
         Loops through all the commands in the help_index dictionary, printing their help description.
        """
        for key in command_dict:
            print(help_dict[key])

    if args is None or args == {}:
        # If the context is default, display the full help page. Context should never otherwise be ' '
        print_all_help()
    else:
        undefined_help = []
        # Recieves a list of different terms following the 'help' term
        for context in args:
            # Loops through each of the recieved terms

            # The normal route for displaying help information for a specific term
            try:
                # Tries to reference the help_index dictionary with the recieved term as the key
                print(help_dict[context])
            except KeyError:
                # Prevents crash:
                # KeyError: '<context>'
                undefined_help.append(context)
        if len(undefined_help) == 0:
            return
        elif len(undefined_help) == 1:
            print(f"Help undefined for '{undefined_help[0]}'.")
        elif len(undefined_help) == 2:
            print(f"Help undefined for '{undefined_help[0]}' and '{undefined_help[1]}'.")
        else:
            unknown_help_string = "Help undefined for "
            for context in undefined_help[:-1]:
                unknown_help_string += context + ', '
            unknown_help_string += 'and ' + undefined_help[len(undefined_help) - 1] + '.'
            print(unknown_help_string)


def clrscrn_command(args=None):
    """
    Clears the console dependent on the operating system
    """
    # https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console
    os.system('cls' if os.name == 'nt' else 'clear')
    if args is not None:
        print(terminal_settings.launch_announcement)


def quit_command(args=None):
    """
     Quit: Safely quits the program and closes the command prompt.
    """
    if args is None:
        quit()


def build_commands(commands_to_add):
    """
    Pass a list of CommandObjects as built below:
    command_handler.CommandObject(cmd_name='',cmd_type=command_handler.CommandType.<TYPE>,cmd_help='',cmd_func=<ref>)
    The cmd_func must have a parameter with 'args=None'
    """
    for new_command in commands_to_add:
        command_dict.update({str.lower(new_command.cmd_name): new_command})
        help_dict.update({str.lower(new_command.cmd_name): new_command.cmd_help})


def command_parser(user_input):
    """
    Splits the user's input into a list based off of spaces, and attempts to interperet what was submitted
    based off of checking a list of single-term and multi-term commands. If the command is recognized in some
    way, it is passed to the applicable command-type interpereter.
    :param user_input:
    """
    user_input_chain = str.split(user_input, ' ')
    # First, check for single-word commands
    if user_input_chain[0] == '':
        # Is the command null/empty?
        return
    if len(user_input_chain) == 1:
        # Is there just one command/term entered?
        try:
            if (command_dict[user_input_chain[0]].cmd_type == CommandType.Single
                    or command_dict[user_input_chain[0]].cmd_type == CommandType.Both):
                # Is the single term recognized as a single-term command?
                interperet_command_single(user_input_chain[0])
            elif command_dict[user_input_chain[0]].cmd_type == CommandType.Multi:
                # The command was recognized as the start of a multi-term command, but there wasn't enough terms
                incomplete_multi_command()
        except KeyError:
            # The command was single term, but it wasn't recognized
            unknown_command()
    else:
        # The command has been determined to be multi-term and thus will be more complex
        try:
            for command in user_input_chain:
                if command_dict[command].cmd_type == CommandType.Single:
                    # Is the single term recognized as a single-term command?
                    interperet_command_single(command)
                elif command_dict[command].cmd_type == CommandType.Both:
                    interperet_command_multiple(user_input_chain)
                    break
                elif command_dict[command].cmd_type == CommandType.Multi:
                    # Is the first term recognized as the start of a multi-term command?
                    interperet_command_multiple(user_input_chain)
                    break
        except KeyError:
            # The command was multi-term, but the first wasn't recognized
            unknown_command()


def interperet_command_single(user_input):
    """
    Recieves a single user input term and attempts to run the command that has the same name as the
    input string. Catches AttributeError as a correct single-term command that isn't yet implemented.
    :param user_input:
    """
    try:
        # https://stackoverflow.com/questions/1855558/call-method-from-string
        # Calls the command from commands.py's Command class based off of the name of the command from user_input
        # getattr(commands.Command, f"{user_input}_command")()
        run_command(user_input)
    except AttributeError:
        # Prevents crash:
        # AttributeError: type object 'Command' has no attribute '<user_input>_command'. Did you mean: 'help_command'?
        print("Recognized single-term command that isn't yet implemented")


def interperet_command_multiple(user_input):
    """
    Recieves a list of user input terms and attempts to run the command associated with the first term recieved,
    Catches AttributeError as a correct multi-term command that isn't yet implemented.
    :param user_input:
    """
    try:
        # https://stackoverflow.com/questions/1855558/call-method-from-string
        # Calls the command from commands.py's Command class based off of the name of the command from user_input
        # Passes all but the first term to the multi-term command
        run_command(user_input[0], user_input[1:])
    except AttributeError:
        # Prevents crash:
        # AttributeError: type object 'Command' has no attribute '<user_input>_command'. Did you mean: 'help_command'?
        print(f"Recognized multi-term command that isn't yet implemented. {user_input}")


command_dict = {}
help_dict = {}
default_commands_to_add = [
    CommandObject(
        cmd_name='Help',
        cmd_type=CommandType.Both,
        cmd_help='Help: Provides amplifying information on whatever is requested. Multiple requests can be '
                 'submitted at the same time.',
        cmd_func=help_command
    ),
    CommandObject(
        cmd_name='Clrscrn',
        cmd_type=CommandType.Single,
        cmd_help='Clrscrn: Clears the command prompt screen.',
        cmd_func=clrscrn_command
    ),
    CommandObject(
        cmd_name='Quit',
        cmd_type=CommandType.Single,
        cmd_help='Quit: Safely quits the program and closes the command prompt.',
        cmd_func=quit_command
    )
]
build_commands(default_commands_to_add)
