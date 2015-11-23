#
# This file is part of The Principles of Modern Game AI.
# Copyright (c) 2015, AiGameDev.com KG.
#

import vispy                    # Main application support.

import window                   # Terminal input and display.


class HAL9000(object):
    
    def __init__(self, terminal):
        """Constructor for the agent, stores references to systems and initializes internal memory.
        """
        self.terminal = terminal
        self.location = 'unknown'
        self._is_initialised = False

    def on_input(self, evt):
        """Called when user types anything in the terminal, connected via event.
        """
        if self._is_initialised:
            if evt.text.startswith('Where am I?'):
                self._log_hal('You are now in the {}, dummy.'.format(self.location))

            else:
                self._log_hal("Your input is registered and won't be taken into mind. Keep trying.")
        else:
            self._log_hal("Good morning, mortal! This is HAL.")
            self._is_initialised = True

    def on_command(self, evt):
        """Called when user types a command starting with `/` also done via events.
        """
        if evt.text == 'quit':
            vispy.app.quit()

        elif evt.text.startswith('relocate'):
            self._log_info('')
            self._log_info('\u2014 Now in the {}. \u2014'.format(evt.text[9:]))
            self.location = evt.text[9:]

        else:
            self._log_error('Command `{}` unknown.'.format(evt.text))    
            self._log_hal("I'm afraid I can't do that.")

    def update(self, _):
        """Main update called once per second via the timer.
        """
        pass

    def _log_hal(self, text, align='right', color='#00805A'):
        self.terminal.log(text, align, color)

    def _log_info(self, text, align='center', color='#404040'):
        self.terminal.log(text, align, color)

    def _log_error(self, text, align='left', color='#ff3000'):
        self.terminal.log(text, align, color)


class Application(object):
    
    def __init__(self):
        # Create and open the window for user interaction.
        self.window = window.TerminalWindow()

        # Print some default lines in the terminal as hints.
        self.window.log('Operator started the chat.', align='left', color='#808080')
        self.window.log('HAL9000 joined.', align='right', color='#808080')

        # Construct and initialize the agent for this simulation.
        self.agent = HAL9000(self.window)

        # Connect the terminal's existing events.
        self.window.events.user_input.connect(self.agent.on_input)
        self.window.events.user_command.connect(self.agent.on_command)

    def run(self):
        timer = vispy.app.Timer(interval=1.0)
        timer.connect(self.agent.update)
        timer.start()
        
        vispy.app.run()


if __name__ == "__main__":
    vispy.set_log_level('WARNING')
    vispy.use(app='glfw')
    
    app = Application()
    app.run()
