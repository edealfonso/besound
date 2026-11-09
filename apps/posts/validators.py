from django.conf import settings
from rest_framework import serializers


def detect_audio_format(head):
    """Return the audio format from the first bytes of a file, or None.

    The file name and the declared content type are not trusted: the
    frontend sends WebM recordings named `.mp3` with type `audio/mp3`.
    """
    if head.startswith(b'\x1a\x45\xdf\xa3'):
        return 'webm'  # Chrome / Firefox MediaRecorder
    if head[4:8] == b'ftyp':
        return 'mp4'  # Safari MediaRecorder (audio/mp4, .m4a)
    if head.startswith(b'ID3') or (len(head) > 1 and head[0] == 0xFF and head[1] & 0xE0 == 0xE0):
        return 'mp3'
    if head.startswith(b'OggS'):
        return 'ogg'
    if head.startswith(b'RIFF') and head[8:12] == b'WAVE':
        return 'wav'
    return None


def validate_audio_file(file):
    max_mb = getattr(settings, 'MAX_AUDIO_UPLOAD_MB', 10)
    if file.size > max_mb * 1024 * 1024:
        raise serializers.ValidationError(f'El audio no puede superar {max_mb} MB.')

    head = file.read(12)
    file.seek(0)
    if detect_audio_format(head) is None:
        raise serializers.ValidationError(
            'El archivo no es un audio válido (se aceptan WebM, MP4/M4A, MP3, OGG y WAV).'
        )
    return file
