"""
The following code takes in the audio file as wav and returns predicted class of the audio,
along with top 10 most probable class.

It uses google's YAMNet in the backend without retraining, ie, Transfer learning.
About YAMNet: YAMNet is a deep net that predicts 521 audio event [classes](https://github.com/tensorflow/models/blob/master/research/audioset/yamnet/yamnet_class_map.csv) from the [AudioSet-YouTube corpus](http://g.co/audioset) it was trained on. It employs the
[Mobilenet_v1](https://arxiv.org/pdf/1704.04861.pdf) depthwise-separable
convolution architecture.

More details aboyt Yamnet can be found here:
Model Card: https://www.kaggle.com/models/google/yamnet/frameworks/tensorFlow2/variations/yamnet/versions/1?tfhub-redirect=true
Transfer Learning tutorial : https://www.tensorflow.org/tutorials/audio/transfer_learning_audio
Construction sound dataset : https://research.google.com/audioset//ontology/tools.html

Functions for plotting the data are added.
"""

import tensorflow as tf  # for creating deep neural networks using Keras Frontend
import tensorflow_hub as hub  # importing hub to use google's pre-trained model(yamnet)
import numpy as np  # using numpy's efficient matrix/arrays operations
import csv  # reading csv files
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # for plotting graphs
from IPython.display import Audio  # for playing audio files in notebooks
import scipy as scipy
from scipy.io import wavfile  # working with audio files

# Load the Model from TensorFlow Hub.
# Note: to read the documentation just follow the model's [url](https://tfhub.dev/google/yamnet/1)

model = hub.load('https://tfhub.dev/google/yamnet/1')


# The labels file will be loaded from the models assets and is present at `model.class_map_path()`.
# You will load it on the `class_names` variable.


# Find the name of the class with the top score when mean-aggregated across frames.
# change this to adjust audio class
def class_names_from_csv(class_map_csv_text):
    """Returns list of class names corresponding to score vector."""
    class_names = []
    with tf.io.gfile.GFile(class_map_csv_text) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            class_names.append(row['display_name'])

    return class_names

# extracting original class names from the CSV file
class_map_path = model.class_map_path().numpy()
class_names = class_names_from_csv(class_map_path)


# Add a method to verify and convert a loaded audio is on the proper sample_rate (16K),
# otherwise it would affect the model's results.
def ensure_sample_rate(original_sample_rate, waveform,
                       desired_sample_rate=16000):
    """Resample waveform if required."""
    if original_sample_rate != desired_sample_rate:
        desired_length = int(round(float(len(waveform)) /
                                   original_sample_rate * desired_sample_rate))
        waveform = scipy.signal.resample(waveform, desired_length)
    return desired_sample_rate, waveform


# Downloading and preparing the sound file
# The expected audio file should be a mono wav file at 16kHz sample rate.

def wav_preprocess(wav_file_name):
    #wav_file
    sample_rate, wav_data = wavfile.read(wav_file_name, 'rb')
    sample_rate, wav_data = ensure_sample_rate(sample_rate, wav_data)

    # show some basic information about the audio.
    duration = len(wav_data) / sample_rate
    print(f'Sample rate: {sample_rate} Hz')
    print(f'Total duration: {duration:.2f}s')
    print(f'Size of the input : {len(wav_data)}')
    size = len(wav_data)

    if len(wav_data.shape) == 1:
        print("The audio is mono.")
        string = "The audio is mono."
    elif len(wav_data.shape) == 2:
        print("The audio is stereo.")
        print(" Converting the audio to mono (by averaging the two channels) for being processsed by Yamnet:")
        string = "The audio is mono."+ " Converting the audio to mono (by averaging the two channels) for being processsed by Yamnet:"
        wav_data = wav_data.mean(axis=1)
    else:
        print("The audio format is not recognized.")
        string = "The audio format is not recognized."
    return wav_data ,sample_rate, duration, size , string


def predict_class(wav_data):
    # normalize the data
    # The `wav_data` needs to be normalized to values in `[-1.0, 1.0]` (as stated in the model's [documentation](https://tfhub.dev/google/yamnet/1)).
    waveform = wav_data / tf.int16.max

    # Run the model, check the output.
    scores, embeddings, spectrogram = model(waveform)

    scores_np = scores.numpy()
    # The spectrogram you will use to do some visualizations later.
    spectrogram_np = spectrogram.numpy()
    infered_class = class_names[scores_np.mean(axis=0).argmax()]

    return infered_class, scores, scores_np, waveform, spectrogram_np


def bar_chart(scores):
    # Let's assume 'scores' is the output from YAMNet and 'class_names' is the list of class names
    # scores.shape -> [num_frames, num_classes]
    # class_names is a list of strings

    # Aggregate scores across all frames
    mean_scores = np.mean(scores, axis=0)

    # Get the top 10 scores and their indices
    top_indices = np.argsort(mean_scores)[-10:][::-1]  # this reverses the order
    top_scores = mean_scores[top_indices]
    top_class_names = [class_names[i] for i in top_indices]

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(top_class_names, top_scores, color='skyblue')
    plt.xlabel('Mean Scores')
    plt.title('Top 10 YAMNet Class Predictions')
    plt.gca().invert_yaxis()  # To display the highest score at the top
    plt.savefig(os.path.join('static', 'bar_chart.png'))
    plt.close()

    #plt.show()

    # In this script, [::-1] is used after np.argsort(mean_scores)[-10:] to reverse the order of the indices,
    # so they are sorted by score in descending order. This, combined with the invert_yaxis(),
    # ensures that the highest values are displayed first in the chart.

    return None

def wave_chart(waveform):
    # Plot the waveform.
    plt.figure(figsize=(10, 6))
    plt.plot(waveform)
    plt.xlim([0, len(waveform)])
    plt.title('Waveform representation of Sound (Averaged Mono-channel')
    plt.xlabel('Time in seconds')
    #plt.show()
    plt.savefig(os.path.join('static', 'waveform.png'))
    plt.close()

    return None

def spectrogram(spectrogram_np):
    # Plot the log-mel spectrogram (returned by the model)
    plt.figure(figsize=(10, 6))
    plt.title('Mel-Spectrogram')
    plt.xlabel('Frequency')
    plt.imshow(spectrogram_np.T, aspect='auto', interpolation='nearest', origin='lower')
    plt.savefig(os.path.join('static', 'spectrogram.png'))
    plt.close()

    #plt.show()

    return None

def graph(scores, scores_np):
    mean_score = np.mean(scores, axis = 0)
    top_n = 10
    top_class_indices = np.argsort(mean_score)[::-1][:top_n]
    plt.figure(figsize=(10, 6))
    plt.title('Representation of confidence scores of network across different classes')
    plt.xlabel('__')
    plt.imshow(scores_np[:, top_class_indices].T, aspect='auto', interpolation= 'nearest' , cmap= 'gray_r')

    # patch_padding = (PATCH_WINDOW_SECONDS / 2) / PATCH_HOP_SECONDS
    # values from the model documentation
    patch_padding = (0.025 / 2) / 0.01
    plt.xlim([-patch_padding - 0.5, scores.shape[0] + patch_padding - 0.5])
    # Label the top_N classes.
    yticks = range(0, top_n, 1)
    plt.yticks(yticks, [class_names[top_class_indices[x]] for x in yticks])
    _ = plt.ylim(-0.5 + np.array([top_n, 0]))

    plt.savefig(os.path.join('static', 'graph.png'))
    plt.close()

    #plt.show()
    return None



def main1 (wav_file_name):
    """
    this function takes care of communicating with the front end and calling all the helper functions
    in the sequence and returns sample rate, duration, size, and print information
    """

    # get the audio file from the front end
    #wav_file_name = file_path
    #wav_file_name = 'drill.wav'
    print(wav_file_name)
    wav_data ,sample_rate, duration, size , string = wav_preprocess(wav_file_name)
    #wav_data = wav_preprocess(wav_file_name)
    # output of the model
    infered_class, scores, scores_np, waveform, spectrogram_np = predict_class(wav_data)

    # visualization and saving to images
    bar_chart(scores)
    wave_chart(waveform)
    spectrogram(spectrogram_np)
    graph(scores, scores_np)

    #return None
    return sample_rate, duration, size, string