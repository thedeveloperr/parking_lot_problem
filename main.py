from input_consumers.file_input_consumer import FileInputConsumer
from command_processor import CommandProcessor
import sys
args = sys.argv
def main():
    input_file = args [1]
    file_input_consumer = FileInputConsumer(CommandProcessor())
    file_input_consumer.consume(input_file)

if __name__ == '__main__':
    main()
