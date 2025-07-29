# Analysis of borg movies
In this md we analyze the borg movies of remnufacturing alternators and starters.

## The main prompt for the movie
Start with uploading the movie `DataIndustrialVideos/borg/Alternators.mp4` to Gemini 2.5 and type the following prompt:
```
Please describe the video in detail. Please include the following in the response:
1. The times for every scene.
2. Describe the setup that is seen in each scene.
3. Provide a a list of the tools that are used in each scene.
4. Provide the actions that are taken in each scene. Name the actions.
```

## The next thing was to get a prompt to transform them to gifs:
```
Suppose the movie is in my command line and called "Alternators.mp4". According to the scenes, write an ffmpeg commands for each scene where the ffmpeg command takes the right times and convert the sliced movie to gif. Provide the list of commands seperated by new line.
```
Result:
```
ffmpeg -i Alternators.mp4 -ss 00:00:00 -to 00:00:10 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" scene1_warehouse.gif

ffmpeg -i Alternators.mp4 -ss 00:00:11 -to 00:00:20 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" scene2_dismantling.gif

ffmpeg -i Alternators.mp4 -ss 00:00:21 -to 00:00:34 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" scene3_housing_washing.gif

ffmpeg -i Alternators.mp4 -ss 00:00:35 -to 00:00:48 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" scene4_stator_cleaning.gif

ffmpeg -i Alternators.mp4 -ss 00:00:49 -to 00:00:58 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" scene5_shaft_grinding.gif

ffmpeg -i Alternators.mp4 -ss 00:00:59 -to 00:01:08 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" scene6_rectifier_preassembly.gif

ffmpeg -i Alternators.mp4 -ss 00:01:09 -to 00:01:30 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" scene7_assembling.gif

ffmpeg -i Alternators.mp4 -ss 00:01:31 -to 00:01:50 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" scene8_performance_test.gif

ffmpeg -i Alternators.mp4 -ss 00:01:51 -to 00:02:08 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" scene9_packaging.gif

ffmpeg -i Alternators.mp4 -ss 00:02:09 -to 00:02:28 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" scene10_conclusion.gif
```

## We wanted refined scenes.
```
Please provide a refined scenes to the movie. Meaning, describing atom actions, where it might be that we have 20-30 scenes.
```
Result:
```
Of course. Here is a refined, more granular breakdown of the video into atomic actions, resulting in 33 distinct scenes.

### Refined Scene Breakdown: Alternators

**Scene 1: Warehouse Dolly Shot**
* **Time:** 00:00 - 00:06
* **Description:** A smooth tracking shot moves forward down a long, narrow aisle of a warehouse, flanked by tall shelves packed with wooden crates of alternator cores.

**Scene 2: Product Comparison**
* **Time:** 00:07 - 00:10
* **Description:** A static shot on a white surface shows a new, shiny remanufactured alternator on the left and an old, dirty core on the right, highlighting the transformation.

**Scene 3: Dismantling Line Overview**
* **Time:** 00:11 - 00:12
* **Description:** A medium shot shows a worker at a disassembly line, with a conveyor belt carrying used alternators.

**Scene 4: Power Tool Disassembly**
* **Time:** 00:13 - 00:16
* **Description:** A close-up shot focuses on the worker's hands using a power driver to quickly remove bolts from an alternator housing.

**Scene 5: Factory Floor High Angle**
* **Time:** 00:17 - 00:18
* **Description:** A high-angle establishing shot provides a brief overview of the bustling factory floor with multiple workstations.

**Scene 6: Disassembled Housings**
* **Time:** 00:19 - 00:20
* **Description:** A close-up shot shows a large bin filled with dirty, disassembled alternator housings awaiting the cleaning process.

**Scene 7: Loading the Industrial Washer**
* **Time:** 00:21 - 00:23
* **Description:** Disassembled housings are shown on a metal tray being loaded onto the conveyor belt of a large, industrial parts washing machine.

**Scene 8: Automated Housing Washing**
* **Time:** 00:24 - 00:30
* **Description:** The camera follows the tray of housings as it moves through the automated washing machine, where they are sprayed and cleaned.

**Scene 9: Post-Wash Housings**
* **Time:** 00:31 - 00:34
* **Description:** A close-up shot reveals a bin full of sparkling clean alternator housings after they have completed the washing cycle.

**Scene 10: Stators Awaiting Cleaning**
* **Time:** 00:35 - 00:38
* **Description:** A shot of a large wire basket filled with alternator stators, identifiable by their copper windings.

**Scene 11: Loading the Media Blaster**
* **Time:** 00:39 - 00:43
* **Description:** A worker in gloves places a single stator into a specialized cleaning machine, closing the door and pressing the start button.

**Scene 12: Stator Media Blasting**
* **Time:** 00:44 - 00:48
* **Description:** An internal close-up of the machine shows the stator's metal frame being cleaned by a fine abrasive spray (media blasting).

**Scene 13: Rotor Setup for Grinding**
* **Time:** 00:49 - 00:51
* **Description:** A worker carefully mounts an alternator rotor into the chuck of a cylindrical grinding machine.

**Scene 14: Rotor Shaft Grinding**
* **Time:** 00:52 - 00:58
* **Description:** A close-up shot captures the rotor shaft spinning as a grinding wheel resurfaces it, creating a shower of sparks. Coolant is applied during the process.

**Scene 15: Rectifier Manual Pre-assembly**
* **Time:** 00:59 - 01:01
* **Description:** A worker's gloved hands are shown manually fitting small components into a rectifier assembly in preparation for pressing.

**Scene 16: Press-Fitting Rectifier Components**
* **Time:** 01:02 - 01:04
* **Description:** The worker places the rectifier into a jig under a press and activates the machine, which presses the components firmly into place.

**Scene 17: Quality Control Graph**
* **Time:** 01:05 - 01:06
* **Description:** A close-up of a monitor screen next to the press displays a graph, confirming the pressure and fit of the newly pressed parts meet specifications.

**Scene 18: Removing Pressed Rectifier**
* **Time:** 01:07 - 01:08
* **Description:** The worker removes the completed rectifier assembly from the press jig.

**Scene 19: Assembly Line Overview**
* **Time:** 01:09 - 01:10
* **Description:** A view of the main assembly line where workers are systematically reassembling the remanufactured alternators.

**Scene 20: Internal Component Assembly**
* **Time:** 01:11 - 01:15
* **Description:** Close-up of a worker inserting internal components into the clean housing and using pliers to secure a piece.

**Scene 21: Soldering Connections**
* **Time:** 01:16 - 01:26
* **Description:** A detailed macro shot shows a worker skillfully using a soldering iron to connect the stator's copper leads to the rectifier terminals, producing plumes of smoke.

**Scene 22: Attaching Rear Cover**
* **Time:** 01:27 - 01:30
* **Description:** A worker fits the black plastic rear cover onto the back of the alternator assembly.

**Scene 23: Loading the Performance Tester**
* **Time:** 01:31 - 01:34
* **Description:** A worker places a fully assembled alternator onto the mounting bracket of an end-of-line performance testing machine.

**Scene 24: Securing and Connecting for Test**
* **Time:** 01:35 - 01:40
* **Description:** The worker tightens clamps to secure the alternator and connects electrical probes to its terminals.

**Scene 25: Initiating Performance Test**
* **Time:** 01:41 - 01:44
* **Description:** The worker closes a protective shield over the unit, and the test begins. A close-up shows the machine's control panel displaying test parameters and results.

**Scene 26: Removing Tested Unit**
* **Time:** 01:45 - 01:50
* **Description:** After the test is complete, the worker opens the shield and removes the performance-verified alternator from the test bench.

**Scene 27: Applying Serial Number**
* **Time:** 01:51 - 01:52
* **Description:** A macro shot shows a worker applying a white label with a unique serial number and QR code to the alternator's casing.

**Scene 28: Applying Quality Seal**
* **Time:** 01:53 - 01:54
* **Description:** The worker applies a round, green sticker with a recycling symbol, signifying it's a remanufactured and quality-approved part.

**Scene 29: Attaching Warning Tag**
* **Time:** 01:55 - 02:00
* **Description:** The worker takes a paper instruction tag with a prominent "STOP" sign and attaches it to the alternator with a rubber band.

**Scene 30: Final Crating**
* **Time:** 02:01 - 02:08
* **Description:** The fully finished, tested, and tagged alternator is carefully placed into a wooden crate for shipping.

**Scene 31: The Old Core**
* **Time:** 02:09 - 02:12
* **Description:** A final, lingering shot of the old, dirty alternator core sitting on the white surface.

**Scene 32: The Remanufactured Product**
* **Time:** 02:13 - 02:19
* **Description:** The shot transitions to the finished, pristine remanufactured alternator, representing the final product of the entire process.

**Scene 33: Brand Outro**
* **Time:** 02:20 - 02:28
* **Description:** The screen fades to black, displaying the "BORG Automotive Reman" logo and the company tagline, "THE MOST IMPORTANT PART IS YOU".
```

## Create a bash script that runs ffmpeg and transform all the scenes to gifs
