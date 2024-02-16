# JUCE Audio Plugin Template Repo

Jump-start your [JUCE / C++](https://github.com/juce-framework/JUCE) audio plugin development with this template repository!

Inspired by [WolfSound's template repo](https://github.com/JanWilczek/audio-plugin-template), with some extra nice additions.

* CMake project for the [JUCE / C++ Framework](https://github.com/juce-framework/JUCE) ready to build and deploy as VST3 / AU, working on Windows & Mac
* Uses CPM to auto-download JUCE
* Default implementation is a functioning gain slider
* Automatic file & folder detection using a custom python script, integrated into the CMake build pipeline. No more manual path entries. Requires Python.
* Automatic build of JUCE's AudioPluginHost project, integrated into the CMake build process.

All plugin's source is under plugin/

All extra tools (python, plugin host save file), under tools/

#### Recommended usage:

* Open the project with a CMake-compatible IDE (ex: VS Community, CLion)
* Build the CMake project, this will download and build all dependencies. This can be automatically handled by your IDE.
* Write your plugin!
* Build the solution and run your plugin using the auto-built AudioPluginHost project, under libs/juce/extras/AudioPluginHost/Builds/..
* This last step can be added as a build step in your IDE configuration, to massively speed up development

Don't forget to change 'WhoaAudioPlugin' and 'My Plugin Title' in plugin/CMakeLists.txt, to your customized name!