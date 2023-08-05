===========================================
Workbench Timestamps command-line interface
===========================================

Installation
============

1. Install `pipx <https://pipxproject.github.io/pipx/>`__
2. Install fh-fablib

   a. ``pipx install workbench-tst`` if you're happy with the packaged version
   b. ``pipx install --editable git+ssh://git@github.com/matthiask/workbench-tst.git#egg=workbench-tst`` otherwise

3. Create a file named ``.workbench`` in your home folder. It should
   contain the controller URL in the following format::

       [workbench]
       controller = https://workbench.feinheit.ch/timestamps-controller/?token=...


Usage
=====

Stopping a task right now::

    tst stop                    # Bare stop
    tst stop one two three      # Including notes

Stopping some other time::

    tst stop -5                 # 5 Minutes ago
    tst stop 13:30              # At 13:30 exactly
    tst stop -10 one two three  # Splitting 10 minutes ago with notes
    tst stop +15                # Split in 15 minutes

Submitting starts::

    tst start
    tst start -5                # I started 5 minutes ago
    tst start -5 one two three  # I started 5 minutes ago with notes

Show today's timestamps::

    tst list

Show help::

    tst
    tst help
