class FileInputConsumer:
    def __init__(self, processor):
        self.processor = processor

    def consume(self, input_file):
            with open(input_file) as file:
                for command in file:
                    try:
                        command_with_removed_newline_char = command.rstrip()
                        print(self.processor.process(command_with_removed_newline_char))
                    except Exception as e:
                        print(e.msg)
