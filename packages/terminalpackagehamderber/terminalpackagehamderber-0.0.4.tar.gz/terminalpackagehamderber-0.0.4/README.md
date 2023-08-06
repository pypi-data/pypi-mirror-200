# KevTerminal

How to add custom commands:

Define a function that has an args parameter with its default as None.
ex:
    def testcmd(args=None):
        print("test worked")

Add the command to the command_handler by using the build_commands function.
ex:
    command_handler.build_commands([
        command_handler.CommandObject(
            cmd_name='Test',
            cmd_type=command_handler.CommandType.Single,
            cmd_help='Test: Help',
            cmd_func=testcmd)
    ])
