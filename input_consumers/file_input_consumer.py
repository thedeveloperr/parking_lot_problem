class FileInputConsumer:
    def __init__(self, processor):
        self.processor = processor

    def consume(self, input_file):
            with open(input_file) as file:
                for command in file:
                    try:
                        print(self.processor.process(command[:-1]))
                    except Exception as e:
                        print(e.msg)
