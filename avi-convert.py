import subprocess

def convert_avi_to_mp4(vlc_path, input_file, output_file):
    command = [vlc_path, input_file, '--sout', f'#transcode{{vcodec=h264,vb=800,acodec=mp4a,ab=128,channels=2,samplerate=44100}}:std{{access=file,mux=mp4,dst={output_file}}}']
    subprocess.run(command)

# Usage example
vlc_path = 'C:/Program Files/VideoLAN/VLC/vlc.exe'
input_file = 'example.avi'
output_file = 'output.mp4'

convert_avi_to_mp4(vlc_path, input_file, output_file)