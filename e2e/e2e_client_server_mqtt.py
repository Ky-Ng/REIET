import sys
sys.path.append("./library")

import argparse
from MQTTHandler import MQTTHandler
import utils.CallBacks

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--topic_name', "-t", default=MQTTHandler.DEFAULT_TOPIC)
    parser.add_argument('--nativeLanguage', "-l",
                        choices=['en', 'zh', 'terminal'], required=True)
    parser.add_argument('--verbose', '-v', action="store_true")
    args = parser.parse_args()

    # Create callbacks based on language
    if args.nativeLanguage == 'en':
        sendingCallback = [utils.CallBacks.get_input_to_english]
        receivingCallback = [utils.CallBacks.synthesize_speech_english]
    elif args.nativeLanguage == 'zh':
        sendingCallback = [utils.CallBacks.getInputFromChinese]
        receivingCallback = [utils.CallBacks.outputInputChinese]
    else:
        sendingCallback = [utils.CallBacks.getInputFromTerminal]
        receivingCallback = [utils.CallBacks.print_input]

    # Add logging callback
    sendingCallback.append(utils.CallBacks.log_to_transcript)
    receivingCallback.append(utils.CallBacks.log_to_transcript)

    # Add print callback if verbose
    if args.verbose and args.nativeLanguage != 'terminal':
        receivingCallback.append(utils.CallBacks.print_input)

    mqttClient = MQTTHandler(receivingCallback, sendingCallback, topic_name=args.topic_name)

    mqttClient.start()


if __name__ == '__main__':
    main()