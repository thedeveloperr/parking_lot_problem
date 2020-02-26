class FileInputConsumer():
    def __init__(self, processor):
      self.processor = processor

    def consume(self, input_file):
        try:
            with open(input_file) as file:
                for command in file:
                    print(self.processor.process(command[:-1]))
        except Exception as e:
            print(e.msg)
