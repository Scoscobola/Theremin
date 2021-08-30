# Theremin
---

A theremin-esque instrument implemented with opencv, the mediapipe hand model, pyo audio synthesis library, and Tkinter.

Users have the ability to play notes through one octave and have the choice to alter the key and quality of the scale. Raising the middle, ring, and pinky finger will play the third, fifth, and seventh of the chord, respectively. The chord played is always rooted on the note determined by the position of the index finger. Moving pairs of fingers closer together lower the quality of chord tones. For example, if I'm playing a major triad with my index, middle, and ring finger, I can bring my index and middle finger together to flat the third. If I bring my middle and ring finger together, I flat the fifth. In the demo below, I attempt to play a ii-V-I progression. 

https://user-images.githubusercontent.com/63258353/131390283-b9f42b30-a81c-4d77-a3a2-111942eb7a71.mp4
