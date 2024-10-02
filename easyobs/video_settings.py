class VideoSettings:
    def __init__(self, client):
        self.client = client

    @property
    def video_settings(self):
        return self.client.get_video_settings()

    @property
    def fps_numerator(self):
        return self.video_settings.fps_numerator
    
    @property
    def fps_denominator(self):
        return self.video_settings.fps_denominator
    
    @property
    def frame_rate(self):
        return self.fps_numerator / self.fps_denominator
    
    @property
    def base_height(self):
        return self.video_settings.base_height
    
    @property
    def base_width(self):
        return self.video_settings.base_width
    
    @property
    def base_resolution(self):
        return self.base_width, self.base_height
    
    @property
    def output_width(self):
        return self.video_settings.output_width
    
    @property
    def output_height(self):
        return self.video_settings.output_height
    
    @property
    def output_resolution(self):
        return self.video_settings.output_width, self.video_settings.output_height
