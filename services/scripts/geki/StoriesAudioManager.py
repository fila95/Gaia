import glob
import SpeakerManager

class StoriesAudioManager():

    storiesMatrix = []
    numberOfStories = 1

    def __init__(self):

        # creates a new list that contains all the path + name of the file of type mp3
        list_of_file_audio = glob.glop("pathname *.mp3")
        number_of_interaction = len(list_of_file_audio)

        for stories in range(0, self.numberOfStories):
            temporary_list = []
            # for each story it creates a list of size number_of_interaction/numberOfStories
            for part_of_story in range(0, number_of_interaction / self.numberOfStories):
                # (stories*numberOfStories) is used to define the different value of list_of_file_audio
                temporary_list.append(list_of_file_audio[part_of_story + (stories * self.numberOfStories)])
            self.storiesMatrix.append(temporary_list)

    def get_path(self, story, part):
        return self.storiesMatrix[story][part]
