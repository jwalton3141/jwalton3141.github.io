---
layout: post
title: Customising your command line
image: https://jwalton3141.github.io/assets/dotfiles/zsh_prompt.png
---

Your command line is a very powerful tool, and once you've spent a fair amount of time working from it you may wish to customise the way it looks and behaves. Fortunately, it's very easy to do so using so-called dotfiles. At the most basic level you may have encountered these before, most likely in the form of the [```.bashrc```](https://unix.stackexchange.com/a/129144) file.

There are already many excellent write-ups which explain what dotfiles are and explain how you may customise them to get the terminal experience you want (see [here](https://medium.com/@webprolific/getting-started-with-dotfiles-43c3602fd789), [here](https://medium.com/@driesvints/getting-started-with-dotfiles-76bf046d035c) and [here](https://zachholman.com/2010/08/dotfiles-are-meant-to-be-forked/) if you're just getting started). I shall therefore restrict myself to explaining the prompt which I wanted, and how I implemented it. My dotfiles are git controlled and can be found in [this repository](https://github.com/jwalton3141/dotfiles).

## Aesthetics

Dieter Rams, of the well-known electronics manufacturer Braun, once said that "good design is as little design as possible". So, though it's possible to implement many fancy and complicated looking prompts, for the most part I consider them cluttered and impractical. Instead, I wanted my prompt to be uncluttered, simple and functional. A prompt should show exactly the information you're interested in at any one point in time, not more, not less. I really like the simplicity of [this Zsh prompt](https://github.com/sindresorhus/pure), so I went about creating something similar in bash. I also took a lot of inspiration from this [excellent prompt function](https://github.com/dreadatour/dotfiles/blob/97dfc43f4ae3c54fa9afc44eb4f6814f85abca69/.bash_profile#L74).

Below is my prompt at its most basic. As I'm logged in as my usual user and not in an active ssh session, the prompt does not remind me where or who I am. The default user name is defined in ```.bashlocal``` as ```local_username```, and the prompt is set to only display the host if in an active ssh session.

<img width="725" height="441" class="img-responsive" src="/assets/dotfiles/empty_prompt.png" style="display: block; margin-left: auto; margin-right: auto; height: auto">

So we see, once I ssh into a different machine the prompt is set to remind me this. Similarly, I would be reminded if I were to enter a session as a different user.

<img width="725" height="441" src="/assets/dotfiles/host_name.png" style="display: block; margin-left: auto; margin-right: auto; height: auto">

Another quality I desired was the two line prompt. If you're several directories deep and the command you're writing becomes too long, it will be wrapped around onto the next line. This makes the command difficult to read and can be a real pain. It's much more desirable to display your current working directory on one line and your command a separate and new line. The example below shows how this setup avoids wrapping long commands.

<img width="725" height="441" src="/assets/dotfiles/two_lines.png" style="display: block; margin-left: auto; margin-right: auto; height: auto">

## Functionality

So far I've only discussed the aesthetics of the prompt, and a discussion of improved functionality has fallen by the wayside. That's because there are more improvements and tweaks possible than I have time. But if I could make only one change to the bash defaults, it'd be the addition of [ipython-like history](https://help.ubuntu.com/community/UsingTheTerminal#An_extremely_handy_tool_::_Incremental_history_searching) (also called incremental history searching).

Altering ```.inputrc``` in this way saves you a lot of trouble in remembering and typing commands. For example, yesterday I ran the command,
```bash
$ for i in {01..25}; do touch sequence$i/meta.txt; done
````
but today I couldn't remember what it was I ran. Using the incremental history search, all I had to do was enter
```bash
$ for 
```
and hit the up-key to see yesterday's command appear.

## Further reading

As I mentioned above, we've barely scratched the surface in terms of the amount of customisation you can give your command line. For further reading I'd suggest [this excellent curated list](https://github.com/webpro/awesome-dotfiles).

### (FAQ: Are you running macOS?)

No. Though my windows look suspiciously mac-esque, I'm actually running unity on Ubuntu 16.04. [This theme](https://github.com/vooze/arc-black-ubuntu) gives my windows that mac-look. I'm not sure what I'll do when canonical drop unity in 18.04...
