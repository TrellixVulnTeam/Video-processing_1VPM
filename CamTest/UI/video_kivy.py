import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.videoplayer import VideoPlayer

path = 'C:\\Users\\sjms1\\Desktop\\video'

vidlist = []

class ScreenVideo(Screen):
    def vidname(self):
        self.sel = SelectableButton().on_press()
        # video = os.path.join(path, self.sel)
        vidlist = Video_list().data_items_norm
        video = os.path.join(path, vidlist[0])
        print(video)
        return video

    def load_vid(self, video):
        video = self.vidname()
        vid = VideoPlayer(source=video, state='play', options={'allow_stretch': False, 'eos': 'loop'})
        self.add_widget(vid)

    def path_test(self):
        pt = os.path.join(path, 'video.mp4')
        return pt

    def on_leave(self):
        pass


class WindowManager(ScreenManager):
    pass


class Menu(Screen):
    pass


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, Button):
    source = ''
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_release(self, *args):
        App.get_running_app().root.current = "root"

    def on_press(self):
        data = self.text
        self.source = os.path.join(path, data)
        # print(self.source)
        return self.source

    def get_source(self):
        return self.source


class Video_list(Screen):
    data_items_norm = ListProperty([])

    def __init__(self, **kwargs):
        super(Video_list, self).__init__(**kwargs)
        self.get_board()

    def get_board(self):
        self.data_items_norm.append('App_download.mp4')
        self.data_items_norm.append('NORM_200407_215033.mp4')
        self.data_items_norm.append('video.mp4')
        vidlist = self.data_items_norm
        return vidlist

class VideoPlayerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = Menu()
        self.video_list = Video_list()
        self.sv = ScreenVideo()

    def build(self):
        sm = ScreenManager()
        sm.add_widget(self.sv)
        sm.add_widget(self.menu)
        sm.add_widget(self.video_list)
        return sm


ui = Builder.load_file("play.kv")

if __name__ == "__main__":
    VideoPlayerApp().run()

# reference need : https://kivy.org/doc/stable/_modules/kivy/uix/videoplayer.html
# https://github.com/jcomish/kivy-video-app/blob/master/main.py