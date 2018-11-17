from pygame import mixer


class SpeakerManager():

    speaker = mixer

    def __init__(self):

        # initialize the speaker
        self.speaker.init()
        self.speaker.music.set_volume(1.0)


    def stop(self):
        self.speaker.musis.stop()

    def pause(self):
        self.speaker.musis.pause()

    def playAudio(self, path = None):
        if path is None:
            self.speaker.musis.unpause()
        else:
            self.speaker.musis.load(path)
            self.speaker.musis.play()

