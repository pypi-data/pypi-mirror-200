from setuptools import setup

setup(
    name='Audio_Cdvst',
    version='1.0',
    description='Eine Python-Bibliothek zur einfachen Audiowiedergabe und -aufnahme.',
    long_description="""Audio_Cdvst ist eine Python-Bibliothek zur einfachen Audiowiedergabe und -aufnahme. Die Bibliothek bietet Funktionen zum Abspielen von WAV- und MP3-Dateien sowie zur Aufnahme von Audio in einer WAV-Datei. Die Bibliothek umfasst auch eine automatische Spracherkennungsfunktion.

Funktionen:
- Einfache Wiedergabe von WAV- und MP3-Dateien
- Aufnahme von Audio in einer WAV-Datei
- Automatische Erkennung der Sprache des Audios

Verfügbar in Englisch und Deutsch.""",
    long_description_content_type='text/markdown',
    url='https://now4free.de/python/module/Audio_Cdvst',
    author='Philipp Juen',
    author_email='support@now4free.de',
    license='MIT',
    packages=['Audio_Cdvst'],
    install_requires=['pydub', 'SpeechRecognition'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='audio, playback, recording, language recognition',
    project_urls={'Source': 'https://github.com/philippjuen/Audio_Cdvst'},
    package_data={'Audio_Cdvst': ['README.md', 'README_en.md']})
