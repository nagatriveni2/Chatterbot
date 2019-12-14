from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import speech_recognition
import subprocess
import platform

'''   
#output in the form of voice
class VoiceChatBot(ChatBot):

    def speak(self, text):
        if platform.system() == 'Darwin':
            # Use Mac's built-in say command to speak the response
            cmd = ['say', str(text)]

            subprocess.call(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        else:
            subprocess.run(
                'echo "' + str(text) + '" | festival --tts',
                shell=True
            )

    def get_response(self, statement=None, **kwargs):
        response = super().get_response(statement, **kwargs)

        self.speak(response.text)


bot = VoiceChatBot('Example ChatBot')

'''

from chatterbot import ChatBot


bot = ChatBot(
    'Math & Time Bot',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ]
)

#output in the form of text 

trainer = ChatterBotCorpusTrainer(bot)

# Train the chat bot with the entire english corpus
trainer.train('chatterbot.corpus.english')

recognizer = speech_recognition.Recognizer()

while True:
    try:
        with speech_recognition.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            
            print('Say Something')
            audio = recognizer.listen(source)

            recognizer_function = getattr(recognizer, 'recognize_google')

            result = recognizer_function(audio)
            
            bot.get_response(text=result)
            print(bot.get_response(text=result))
    except speech_recognition.UnknownValueError:
        bot.speak('I am sorry, I could not understand that.')
    except speech_recognition.RequestError as e:
        message = 'My speech recognition service has failed. {0}'
        bot.speak(message.format(e))
    except (KeyboardInterrupt, EOFError, SystemExit):
        # Press ctrl-c or ctrl-d on the keyboard to exit
        break
