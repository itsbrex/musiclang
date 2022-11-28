class Item(object):
    def __init__(self, name, start, end, vel=0, pitch=0, track=0, channel=0, voice=0, value=''):
        self.name = name
        self.start = start  # start step
        self.end = end  # end step
        self.vel = vel
        self.pitch = pitch
        self.track = track
        self.channel = channel
        self.voice = voice
        self.value = value


    @classmethod
    def frommatrix(cls, matrix):
        return [Item('', start, end, vel, pitch, track, voice, channel) for start, end, vel, pitch, track, voice, channel in matrix]

    def __repr__(self):
        return f'Item(name={self.name:>10s}, start={self.start}, end={self.end}, ' \
               f'vel={self.vel}, pitch={self.pitch}, track={self.track}, channel={self.channel}, voice={self.voice},' \
               f'value={self.value})\n'

    def __eq__(self, other):
        return self.name == other.name and self.start == other.start and \
               self.pitch == other.pitch and self.track == other.track

    def array(self):
        return [self.start, self.end, self.vel, self.pitch, self.track, self.channel, self.voice]