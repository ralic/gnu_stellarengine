#!/usr/bin/env python

# Stellar Game Engine Template
# Copyright (C) 2012, 2013 Julian Marchant <onpon4@lavabit.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Stellar Game Engine - [insert implementation name here]

Stellar Game Engine is a library for Stellar.  It is a game engine
loosely based on Game Maker.

Except where otherwise noted, all documented features are required to be
offered by all implementations.  Any implementation failing to do so is
incomplete.

Constants:
    IMPLEMENTATION: A string identifying the how the engine is
        implemented (e.g. the name of the graphics library used).
    ALIGN_LEFT: Flag indicating alignment to the left.
    ALIGN_CENTER: Flag indicating alignment to the horizontal center.
    ALIGN_RIGHT: Flag indicating alignment to the right.
    ALIGN_TOP: Flag indicating alignment to the top.
    ALIGN_MIDDLE: Flag indicating alignment to the vertical middle.
    ALIGN_BOTTOM: Flag indicating alignment to the bottom.

Global variables:
    game: Stores the current game.  If there is no game currently, this
        variable is set to None.

Classes:
    Game: Class which handles the game.
    Sprite: Class used to store images and animations.
    BackgroundLayer: Class used to store a background layer.
    Background: Class used to store parallax-scrolling backgrounds.
    Font: Class used to store and handle fonts.
    Sound: Class used to store and play sound effects.
    Music: Class used to store and play music.
    StellarClass: Class used for game objects.
    Room: Class used for game rooms, e.g. levels.
    View: Class used for views in rooms.

Implementation-specific information:
[insert info here]

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.0.20"

import sys
import os
import math
import json

# Import implementation-specific libraries like Pygame here

__all__ = ['Game', 'Sprite', 'BackgroundLayer', 'Background', 'Font', 'Sound',
           'Music', 'StellarClass', 'Room', 'View', 'game', 'ALIGN_LEFT',
           'ALIGN_CENTER', 'ALIGN_RIGHT', 'ALIGN_TOP', 'ALIGN_MIDDLE',
           'ALIGN_BOTTOM']
# Except in extreme cases, these constants should not be modified.
DEFAULT_SCREENWIDTH = 640
DEFAULT_SCREENHEIGHT = 480
DEFAULT_FULLSCREEN = False
DEFAULT_SCALE = 0
DEFAULT_SCALE_PROPORTIONAL = True
DEFAULT_SCALE_SMOOTH = False
DEFAULT_FPS = 60
DEFAULT_DELTA = False
DEFAULT_DELTA_MIN = 15
COLORS = {'white': '#ffffff', 'silver': '#c0c0c0', 'gray': '#808080',
          'black': '#000000', 'red': '#ff0000', 'maroon': '#800000',
          'yellow': '#ffff00', 'olive': '#808000', 'lime': '#00ff00',
          'green': '#008000', 'aqua': '#00ffff', 'teal': '#008080',
          'blue': '#0000ff', 'navy': '#000080', 'fuchsia': '#ff00ff',
          'purple': '#800080'}
COLORNAMES = {}
for pair in COLORS.items():
    COLORNAMES[pair[1]] = pair[0]

KEYS = {"0": None, "1": None, "2": None, "3": None, "4": None, "5": None, "6": None, "7": None, "8": None, "9": None, "a": None, "b": None, "c": None, "d": None, "e": None, "f": None, "g": None, "h": None, "i": None, "j": None, "k": None, "l": None, "m": None, "n": None, "o": None, "p": None, "q": None, "r": None, "s": None, "t": None, "u": None, "v": None, "w": None, "x": None, "y": None, "z": None, "alt_left": None, "alt_right": None, "ampersand": None, "apostrophe": None, "asterisk": None, "at": None, "backslash": None, "backspace": None, "backtick": None, "bracket_left": None, "bracket_right": None, "break": None, "caps_lock": None, "caret": None, "clear": None, "colon": None, "comma": None, "ctrl_left": None, "ctrl_right": None, "delete": None, "dollar": None, "down": None, "end": None, "enter": None, "equals": None, "escape": None, "euro": None, "exclamation": None, "f1": None, "f2": None, "f3": None, "f4": None, "f5": None, "f6": None, "f7": None, "f8": None, "f9": None, "f10": None, "f11": None, "f12": None, "greater_than": None, "hash": None, "help": None, "home": None, "hyphen": None, "insert": None, "kp_0": None, "kp_1": None, "kp_2": None, "kp_3": None, "kp_4": None, "kp_5": None, "kp_6": None, "kp_7": None, "kp_8": None, "kp_9": None, "kp_divide": None, "kp_enter": None, "kp_equals": None, "kp_minus": None, "kp_multiply": None, "kp_plus": None, "kp_point": None, "left": None, "less_than": None, "menu":None, "meta_left":None, "meta_right":None, "mode":None, "num_lock":None, "pagedown":None, "pageup":None, "parenthesis_left":None, "parenthesis_right":None, "pause":None, "period":None, "plus":None, "power":None, "print_screen":None, "question":None, "quote":None, "right":None, "scroll_lock":None, "semicolon":None, "shift_left":None, "shift_right":None, "slash":None, "space":None, "super_left":None, "super_right":None, "sysrq":None, "tab":None, "underscore":None, "up":None}
KEYNAMES = {}
for pair in KEYS.items():
    KEYNAMES[pair[1]] = pair[0]

IMPLEMENTATION = "Template"
ALIGN_LEFT = 2
ALIGN_CENTER = 3
ALIGN_RIGHT = 1
ALIGN_TOP = 2
ALIGN_MIDDLE = 3
ALIGN_BOTTOM = 1

# Global variables
game = None


class Game(object):

    """Class which handles the game.

    A Game object must be created before anything else is done.

    All Game objects have the following attributes:
        width: The width of the game's display in pixels.
        height: The height of the game's display in pixels.
        fullscreen: True if the game should be in fullscreen, False
            otherwise.
        scale: A number indicating a fixed scale factor (e.g. 1 for no
            scaling, 2 for doubled size).  If set to 0, scaling is
            automatic (causes the game to fit the window or screen).
        scale_proportional: If set to True, scaling is always
            proportional.  If set to False, the image may be stretched
            to completely fill the game window or screen.  This has no
            effect unless ``scale`` is 0.
        scale_smooth: If set to True, a smooth scaling algorithm will be
            used, if available.  Otherwise, simple scaling (e.g. pixel
            doubling) will always be used.  Support for smooth scaling
            in Stellar Game Engine implementations is optional.  If the
            implementation used does not support smooth scaling, this
            option will always be treated as False.
        fps: The rate the game should run in frames per second.  Note
            that this is only the maximum; if the computer is not fast
            enough, the game may run more slowly.
        delta: If set to True, delta timing will be enabled, which
            adjusts speeds and animation rates if the game cannot run at
            the specified frame rate.
        delta_min: Delta timing can cause the game to be choppy.  This
            setting limits this by pretending that the frame rate is
            never lower than this amount, resulting in the game slowing
            down like normal if it is.

    The following read-only attributes are also available:
        sprites: A dictionary containing all loaded sprites, using their
            names as the keys.
        background_layers: A dictionary containing all loaded background
            layers, using their sprites' names as the keys.
        backgrounds: A dictionary containing all loaded backgrounds,
            using their unique identifiers as the keys.
        fonts: A dictionary containing all loaded fonts, using their
            names as the keys.
        sounds: A dictionary containing all loaded sounds, using their
            file names as the keys.
        music: A dictionary containing all loaded music, using their
            file names as the keys.
        objects: A dictionary containing all StellarClass objects in the
            game, using their unique identifiers as the keys.
        rooms: A list containing all rooms in order of their creation.
        current_room: The Room object which is currently active.
        mouse: A StellarClass object which represents the mouse cursor.
            Its ID is "mouse" and its bounding box is one pixel.
            Speed variables are determined by averaging all mouse
            movement during the last quarter of a second.  Assigning to
            its ``visible`` attribute controls whether or not the mouse
            cursor is shown.  Setting its sprite sets the mouse cursor.

    Game methods:
        start: Start the game at the first room.
        end: Properly end the game.
        pause: Pause the game.
        unpause: Unpause the game.
        draw_dot: Draw a single-pixel dot.
        draw_line: Draw a line segment between the given points.
        draw_rectangle: Draw a rectangle at the given position.
        draw_ellipse: Draw an ellipse at the given position.
        draw_circle: Draw a circle at the given position.
        sound_stop_all: Stop playback of all sounds.
        get_key_pressed: Return whether or not a given key is pressed.
        get_mouse_button_pressed: Return whether or not a given mouse
            button is pressed.
        get_joystick_axis: Return the position of the given axis.
        get_joystick_hat: Return the position of the given HAT.
        get_joystick_button_pressed: Return whether or not the given
            joystick button is pressed.
        get_joysticks: Return the number of joysticks available.
        get_joystick_axes: Return the number of axes on the given
            joystick.
        get_joystick_hats: Return the number of HATs on the given
            joystick.
        get_joystick_buttons: Return the number of buttons on the
            given joystick.

    Game events are handled by special methods.  The time that they are
    called is based on the following events, which happen each frame in
    the following order and are synchronized among all objects which
    have them:
        event_step_begin
        event_step
        event_step_end

    The following events are not timed in any particular way, but are
    called immediately when the engine detects them occurring:
        event_game_start
        event_game_end
        event_paused_key_press
        event_paused_key_release
        event_paused_mouse_move
        event_paused_mouse_button_press
        event_paused_mouse_button_release
        event_paused_joystick_axis_move
        event_paused_joystick_hat_move
        event_paused_joystick_button_press
        event_paused_joystick_button_release
        event_paused_close

    The following events are always called (in no particular order)
    between calls of event_step_begin and event_step:
        event_key_press
        event_key_release
        event_mouse_move
        event_mouse_button_press
        event_mouse_button_release
        event_joystick_axis_move
        event_joystick_hat_move
        event_joystick_button_press
        event_joystick_button_release
        event_close

    The following events are always called (in no particular order)
    between calls of event_step and event_step_end:
        event_mouse_collision
        event_mouse_collision_left
        event_mouse_collision_right
        event_mouse_collision_top
        event_mouse_collision_bottom

    """

    def __init__(self, width=DEFAULT_SCREENWIDTH, height=DEFAULT_SCREENHEIGHT,
                 fullscreen=DEFAULT_FULLSCREEN, scale=DEFAULT_SCALE,
                 scale_proportional=DEFAULT_SCALE_PROPORTIONAL,
                 scale_smooth=DEFAULT_SCALE_SMOOTH, fps=DEFAULT_FPS,
                 delta=DEFAULT_DELTA, delta_min=DEFAULT_DELTA_MIN):
        """Create a new Game object.

        Arguments set the properties of the game.  See Game.__doc__ for
        more information.

        """
        global game
        game = self

    def start(self):
        """Start the game at the first room.

        Can be called in the middle of a game to start the game over.
        If you do this, everything will be reset to its original state.

        """
        pass

    def end(self):
        """Properly end the game."""
        global game
        game = None

    def pause(self, image=None):
        """Pause the game.

        ``image`` is the image to show when the game is paused.  If set
        to None, the default image will be shown.  The default image is
        at the discretion of the Stellar Game Engine implementation, as
        are any additional visual effects, with the stipulation that the
        following conditions are met:

            1. The default image must unambiguously demonstrate that the
                game is paused (the easiest way to do this is to include
                the word "paused" somewhere in the image).
            2. The view must stay in place.
            3. What was going on within the view before the game was
                paused must remain visible while the game is paused.

        While the game is paused, all game events will be halted, all
        objects will be treated like they don't exist, and all sounds
        and music will be stopped.  Game events whose names start with
        "event_paused_" will occur during this time.

        """
        pass

    def unpause(self):
        """Unpause the game."""
        pass

    def draw_dot(self, x, y, z, color):
        """Draw a single-pixel dot.

        ``x`` and ``y`` indicate the location in the room to draw the
        dot, where the left and top edges of the room are 0 and x and y
        increase toward the right and bottom.  ``z`` indicates the
        Z-axis position to draw the dot, where a higher Z value is
        closer to the viewer.  ``color`` indicates the color of the dot.

        """
        pass

    def draw_line(self, x1, y1, x2, y2, z, color, thickness=1,
                  anti_alias=False):
        """Draw a line segment between the given points.

        ``x1``, ``y1``, ``x2``, and ``y2`` indicate the location in the
        room of the points between which to draw the line segment, where
        the left and top edges of the room are 0 and x and y increase
        toward the right and bottom.  ``z`` indicates the Z-axis
        position to draw the line, where a higher Z value is closer to
        the viewer.  ``color`` indicates the color of the line segment.
        ``thickness`` indicates the thickness of the line segment in
        pixels.  ``anti_alias`` indicates whether or not anti-aliasing
        should be used.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this function will act like ``anti_alias`` is
        False.

        """
        pass

    def draw_rectangle(self, x, y, z, width, height, fill=None, outline=None,
                       outline_thickness=1):
        """Draw a rectangle at the given position.

        ``x`` and ``y`` indicate the location in the room to position
        the top-left corner of the rectangle, where the left and top
        edges of the room are 0 and x and y increase toward the right
        and bottom.  ``z`` indicates the Z-axis position to draw the
        rectangle, where a higher Z value is closer to the viewer.
        ``width`` and ``height`` indicate the size of the rectangle.
        ``fill`` indicates the color of the fill of the rectangle; set
        to None for no fill.  ``outline`` indicates the color of the
        outline of the rectangle; set to None for no outline.
        ``outline_thickness`` indicates the thickness of the outline in
        pixels (ignored if there is no outline).

        """
        pass

    def draw_ellipse(self, x, y, z, width, height, fill=None, outline=None,
                     outline_thickness=1, anti_alias=False):
        """Draw an ellipse at the given position.

        ``x`` and ``y`` indicate the location in the room to position
        the top-left corner of the imaginary rectangle containing the
        ellipse, where the left and top edges of the room are 0 and x
        and y increase toward the right and bottom.  ``z`` indicates the
        Z-axis position to draw the ellipse, where a higher Z value is
        closer to the viewer.  ``width`` and ``height`` indicate the
        size of the ellipse.  ``fill`` indicates the color of the fill
        of the ellipse; set to None for no fill.  ``outline`` indicates
        the color of the outline of the ellipse; set to None for no
        outline.  ``outline_thickness`` indicates the thickness of the
        outline in pixels (ignored if there is no outline).
        ``anti_alias`` indicates whether or not anti-aliasing should be
        used on the outline.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this function will act like ``anti_alias`` is
        False.

        """

    def draw_circle(self, x, y, z, radius, fill=None, outline=None,
                    outline_thickness=1):
        """Draw a circle at the given position.

        ``x`` and ``y`` indicate the location in the room to position
        the center of the circle, where the left and top edges of the
        room are 0 and x and y increase toward the right and bottom.
        ``z`` indicates the Z-axis position to draw the circle, where a
        higher Z value is closer to the viewer.  ``radius`` indicates
        the radius of the circle in pixels.  ``fill`` indicates the
        color of the fill of the circle; set to None for no fill.
        ``outline`` indicates the color of the outline of the circle;
        set to None for no outline.  ``outline_thickness`` indicates the
        thickness of the outline in pixels (ignored if there is no
        outline).  ``anti_alias`` indicates whether or not anti-aliasing
        should be used on the outline.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this function will act like ``anti_alias`` is
        False.

        """

    def sound_stop_all(self):
        """Stop playback of all sounds."""
        pass

    def get_key_pressed(self, key):
        """Return whether or not a given key is pressed.

        ``key`` is the key to check.

        """
        pass

    def get_mouse_button_pressed(self, button):
        """Return whether or not a given mouse button is pressed.

        ``button`` is the number of the mouse button to check, where 0
        is the first mouse button.

        """
        pass

    def get_joystick_axis(self, joystick, axis):
        """Return the position of the given axis.

        ``joystick`` is the number of the joystick to check, where 0 is
        the first joystick.  ``axis`` is the number of the axis to
        check, where 0 is the first axis of the joystick.

        Returned value is a float from -1 to 1, where 0 is centered, -1
        is all the way to the left or up, and 1 is all the way to the
        right or down.

        If the joystick or axis requested does not exist, 0 is returned.

        Support for joysticks in Stellar Game Engine implementations is
        optional.  If the implementation used does not support
        joysticks, this function will act like the joystick requested
        does not exist.

        """
        pass

    def get_joystick_hat(self, joystick, hat):
        """Return the position of the given HAT.

        ``joystick`` is the number of the joystick to check, where 0 is
        the first joystick.  ``hat`` is the number of the HAT to check,
        where 0 is the first HAT of the joystick.

        Returned value is a tuple in the form (x, y), where x is the
        horizontal position and y is the vertical position.  Both x and
        y are 0 (centered), -1 (left or up), or 1 (right or down).

        If the joystick or HAT requested does not exist, (0, 0) is
        returned.

        Support for joysticks in Stellar Game Engine implementations is
        optional.  If the implementation used does not support
        joysticks, this function will act like the joystick requested
        does not exist.

        """
        pass

    def get_joystick_button_pressed(self, joystick, button):
        """Return whether or not the given button is pressed.

        ``joystick`` is the number of the joystick to check, where 0 is
        the first joystick.  ``button`` is the number of the button to
        check, where 0 is the first button of the joystick.

        If the joystick or button requested does not exist, False is
        returned.

        Support for joysticks in Stellar Game Engine implementations is
        optional.  If the implementation used does not support
        joysticks, this function will act like the joystick requested
        does not exist.

        """
        pass

    def get_joysticks(self):
        """Return the number of joysticks available.

        Support for joysticks in Stellar Game Engine implementations is
        optional.  If the implementation used does not support
        joysticks, this function will always return 0.

        """
        pass

    def get_joystick_axes(self, joystick):
        """Return the number of axes available on the given joystick.

        ``joystick`` is the number of the joystick to check, where 0 is
        the first joystick.  If the given joystick does not exist, 0
        will be returned.

        Support for joysticks in Stellar Game Engine implementations is
        optional.  If the implementation used does not support
        joysticks, this function will act like the joystick requested
        does not exist.

        """
        pass

    def get_joystick_hats(self, joystick):
        """Return the number of HATs available on the given joystick.

        ``joystick`` is the number of the joystick to check, where 0 is
        the first joystick.  If the given joystick does not exist, 0
        will be returned.

        Support for joysticks in Stellar Game Engine implementations is
        optional.  If the implementation used does not support
        joysticks, this function will act like the joystick requested
        does not exist.

        """
        pass

    def get_joystick_buttons(self, joystick):
        """Return the number of buttons available on the given joystick.

        ``joystick`` is the number of the joystick to check, where 0 is
        the first joystick.  If the given joystick does not exist, 0
        will be returned.

        Support for joysticks in Stellar Game Engine implementations is
        optional.  If the implementation used does not support
        joysticks, this function will act like the joystick requested
        does not exist.

        """
        pass

    def event_game_start(self):
        """Game start event."""
        pass

    def event_game_end(self):
        """Game end event."""
        pass

    def event_paused_key_press(self, key):
        """Key press event when paused.

        See event_key_press.__doc__ for more information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See event_key_release.__doc__ for more information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See event_mouse_move.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See event_mouse_button_press.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See event_mouse_button_release.__doc__ for more information.

        """
        pass

    def event_paused_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when paused.

        See event_joystick_axis_move.__doc__ for more information.

        """
        pass

    def event_paused_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when paused.

        See event_joystick_hat_move.__doc__ for more information.

        """
        pass

    def event_paused_joystick_button_press(self, joystick, button):
        """Joystick button press event when paused.

        See event_joystick_button_press.__doc__ for more information.

        """
        pass

    def event_paused_joystick_button_release(self, joystick, button):
        """Joystick button release event when paused.

        See event_joystick_button_release.__doc__ for more information.

        """
        pass

    def event_paused_close(self):
        """Close event (e.g. close button) when paused."""
        pass

    def event_step_begin(self):
        """Global begin step event."""
        pass

    def event_key_press(self, key):
        """Key press event.

        ``key`` is the key that was pressed.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        ``key`` is the key that was pressed.

        """
        pass

    def event_mouse_move(self, x, y):
        """Mouse move event.

        ``x`` and ``y`` indicate the relative movement of the mouse.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        ``button`` is the number of the mouse button that was pressed,
        where 0 is the first mouse button.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        ``button`` is the number of the mouse button that was released,
        where 0 is the first mouse button.

        """
        pass

    def event_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``axis`` is the number of the axis, where 0 is the
        first axis.  ``value`` is the tilt of the axis, where 0 is in
        the center, -1 is tilted all the way to the left or up, and 1 is
        tilted all the way to the right or down.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``hat`` is the number of the HAT, where 0 is the
        first HAT.  ``x`` and ``y`` indicate the position of the HAT,
        where 0 is in the center, -1 is left or up, and 1 is right or
        down.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_button_press(self, joystick, button):
        """Joystick button press event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``button`` is the number of the button pressed, where
        0 is the first button.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_button_release(self, joystick, button):
        """Joystick button release event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``button`` is the number of the button pressed, where
        0 is the first button.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_close(self):
        """Close event (e.g. close button)."""
        pass

    def event_step(self):
        """Global step event."""
        pass

    def event_mouse_collision(self, other):
        """Middle/default mouse collision event."""
        pass

    def event_mouse_collision_left(self, other):
        """Left mouse collision event."""
        self.event_mouse_collision(other)

    def event_mouse_collision_right(self, other):
        """Right mouse collision event."""
        self.event_mouse_collision(other)

    def event_mouse_collision_top(self, other):
        """Top mouse collision event."""
        self.event_mouse_collision(other)

    def event_mouse_collision_bottom(self, other):
        """Bottom mouse collision event."""
        self.event_mouse_collision(other)

    def event_step_end(self):
        """Global end step event."""
        pass


class Sprite(object):

    """Class which holds information for images and animations.

    All Sprite objects have the following attributes:
        width: The width of the sprite in pixels.
        height: The height of the sprite in pixels.
        origin_x: The horizontal location of the origin (the pixel
            position in relation to the images to base rendering on),
            where the left edge of the image is 0 and origin_x increases
            toward the right.
        origin_y: The vertical location of the origin (the pixel
            position in relation to the images to base rendering on),
            where the top edge of the image is 0 and origin_y increases
            toward the bottom.
        transparent: True if the image should support transparency,
            False otherwise.  If the image does not have an alpha
            channel or if the implementation used does not support alpha
            transparency, a colorkey will be used, with the transparent
            color being the color of the top-rightmost pixel.
        fps: The suggested rate in frames per second to animate the
            image at.
        bbox_x: The horizontal location of the top-left corner of the
            suggested bounding box to use with this sprite, where
            origin_x is 0 and bbox_x increases toward the right.
        bbox_y: The vertical location of the top-left corner of the
            suggested bounding box to use with this sprite, where
            origin_y is 0 and bbox_y increases toward the bottom.
        bbox_width: The width of the suggested bounding box in pixels.
        bbox_height: The height of the suggested bounding box in pixels.

    The following read-only attributes are also available:
        name: The name of the sprite given when it was created.  See
            Sprite.__init__.__doc__ for more information.

    """

    def __init__(self, name, width=None, height=None, origin_x=0, origin_y=0,
                 transparent=True, fps=DEFAULT_FPS, bbox_x=0, bbox_y=0,
                 bbox_width=None, bbox_height=None):
        """Create a new Sprite object.

        ``name`` indicates the base name of the image files.  Files are
        to be located in data/images, data/sprites, or data/backgrounds.
        If a file with the exact name plus image file extensions is not
        available, numbered images will be searched for which have names
        with one of the following formats, where "name" is replaced with
        the specified base file name and "0" can be replaced with any
        integer:

            name-0
            name_0

        If images are found with names like those, all such images will
        be loaded and become frames of animation.  If not, sprite sheets
        will be searched for which have names with one of the following
        formats, where "name" is replaced with the specified base file
        name and "2" can be replaced with any integer:

            name-strip2
            name_strip2

        The number indicates the number of animation frames in the
        sprite sheet. The sprite sheet will be read like a horizontal
        reel, with the first frame on the far left and the last frame on
        the far right, and no space in between frames.

        If no image is found based on any of the above methods, a black
        rectangle will be created at the size specified by ``width`` and
        ``height``.  If either ``width`` or ``height`` is None, the
        respective size will default to 16 in this case.

        If ``width`` or ``height`` is set to None, the respective size
        will be taken from the largest animation frame.  If
        ``bbox_width`` or ``bbox_height`` is set to None, the respective
        size will be the respective size of the sprite.

        All remaining arguments set the initial properties of the
        sprite; see Sprite.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        # This is a way to figure out what image to load.
        assert name

        fnames = os.listdir(os.path.join('data', 'images'))
        fnames.extend(os.listdir(os.path.join('data', 'sprites')))
        fnames.extend(os.listdir(os.path.join('data', 'backgrounds')))
        fname_single = None
        fname_frames = []
        fname_strip = None

        for fname in fnames:
            if fname.startswith(name) and os.path.isfile(fname):
                root, ext = os.path.splitext(fname)
                if root.rsplit('-', 1)[0] == name:
                    split = root.rsplit('-', 1)
                elif root.split('_', 1)[0] == name:
                    split = root.rsplit('_', 1)
                else:
                    split = (name, '')

                if root == name:
                    fname_single = fname
                elif split[1].isdigit():
                    n = int(split[1])
                    while len(fname_frames) - 1 < n:
                        fname_frames.append(None)
                    fname_frames[n] = fname
                elif (split[1].startswith('strip') and split[1][5:].isdigit()):
                    fname_strip = fname

        if fname_single:
            # Load the single image
            pass

        elif any(fname_frames):
            # Load the multiple images
            for fname in fname_frames:
                if fname:
                    pass

        elif fname_strip:
            # Load the strip (sprite sheet)
            root, ext = os.path.splitext(fname)
            assert '-' in root or '_' in root
            assert (root.rsplit('-', 1)[0] == name or
                    root.rsplit('_', 1)[0] == name)
            if root.rsplit('-', 1)[0] == name:
                split = root.rsplit('-', 1)
            else:
                split = root.rsplit('_', 1)

            # Load sheet here

        else:
            # Generate placeholder image
            pass


class BackgroundLayer(object):

    """Special class used for background layers.

    All BackgroundLayer objects have the following attributes:
        sprite: The Sprite object used for this layer.  While it will
            always be an actual Sprite object when read, it can also be
            set to the ID of a sprite.
        x: The horizontal offset of the layer.
        y: The vertical offset of the layer.
        z: The Z-axis position of the layer in the room, which
            determines in what order layers are drawn; layers with a
            higher Z value are drawn in front of layers with a lower Z
            value.
        xscroll_rate: The horizontal speed the layer scrolls as a factor
            of the view scroll speed.
        yscroll_rate: The vertical speed the layer scrolls as a factor
            of the view scroll speed.
        xrepeat: Whether or not the background should be repeated
            horizontally.
        yrepeat: Whether or not the background should be repeated
            vertically.

    """

    def __init__(self, sprite, x, y, z, xscroll_rate=1, yscroll_rate=1,
                 xrepeat=True, yrepeat=True):
        """Create a background layer object.

        Arguments set the properties of the layer.  See
        BackgroundLayer.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        pass


class Background(object):

    """Background class.

    All Background objects have the following attributes:
        color: A Stellar Game Engine color used in parts of the
            background where there is no layer.

    The following read-only attributes are also available:
        id: The unique identifier for this background.
        layers: A tuple containing all BackgroundLayer objects used in
            this background.

    """

    def __init__(self, layers, color, id_=None, **kwargs):
        """Create a background with the given color and layers.

        Arguments set the properties of the background.  See
        Background.__doc__ for more information.

        If ``id`` is None, it will be set to an integer not currently
        used as an ID (the exact number chosen is implementation-
        specific and may not necessarily be the same between runs).

        In addition to containing actual BackgroundLayer objects,
        ``layers`` can contain valid names of BackgroundLayer objects'
        sprites.

        A game object must exist before an object of this class is
        created.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        if 'id' in kwargs:
            id_ = kwargs['id']


class Font(object):

    """Font handling class.

    All Font objects have the following attributes:
        name: The name of the font.  Set to None for the default font.
        size: The height of the font in pixels.
        underline: Whether or not underlined rendering is enabled.
        bold: Whether or not bold rendering is enabled.
        italic: Whether or not italic rendering is enabled.

    """

    def __init__(self, name=None, size=12, underline=False, bold=False,
                 italic=False):
        """Create a new Font object.

        Arguments set the properties of the font.  See
        Font.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        pass

    def render(self, text, x, y, width=None, height=None, color="black",
               halign=ALIGN_LEFT, valign=ALIGN_TOP, anti_alias=True):
        """Render the given text to the screen.

        ``text`` indicates the text to render.  ``x`` and ``y`` indicate
        the location in the room to render the text, where the left and
        top edges of the room are 0 and x and y increase toward the
        right and bottom.  ``width`` and ``height`` indicate the size of
        the imaginary box the text is drawn in; set to None for no
        imaginary box.  ``color`` indicates the color of the text.
        ``halign`` indicates the horizontal alignment and can be
        ALIGN_LEFT, ALIGN_CENTER, or ALIGN_RIGHT. ``valign`` indicates
        the vertical alignment and can be ALIGN_TOP, ALIGN_MIDDLE, or
        ALIGN_BOTTOM.  ``anti_alias`` indicates whether or not
        anti-aliasing should be used.

        If the text does not fit in the imaginary box specified,
        ``height`` will be treated as None (i.e. the imaginary box will
        be vertically resized to fit the text).

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this function will act like ``anti_alias`` is False.

        """
        pass

    def get_size(self, text, x, y, width=None, height=None):
        """Return the size of the given rendered text.

        All arguments correspond with the same arguments in Font.render,
        and the size returned reflects rendering rules therein; see
        Font.render.__doc__ for more information.  Returned value is a
        tuple in the form (width, height).

        """
        pass


class Sound(object):

    """Sound handling class.

    All Sound objects have the following attributes:
        volume: The volume of the sound in percent (0 for no sound, 100
            for max sound).
        balance: The balance of the sound effect on stereo speakers.  A
            value of 0 means centered (an equal amount of play on both
            speakers), -1 means entirely in the left speaker, and 1
            means entirely in the right speaker.  Support for this
            feature in Stellar Game Engine implementations is optional.
            If it is unavailable, all sounds will be played through both
            speakers equally (assuming stereo sound is used).
        max_play: The maximum instances of this sound playing permitted.
            Set to 0 for no limit.
        length: The length of the sound in milliseconds.
        playing: The number of instances of this sound playing.

    The following read-only attributes are also available:
        fname: The file name of the sound given when it was created.
            See Sound.__init__.__doc__ for more information.

    Sound methods:
        Sound.play: Play the sound.
        Sound.stop: Stop the sound.
        Sound.pause: Pause playback of the sound.
        Sound.unpause: Resume playback of the sound if paused.

    Ogg Vorbis and uncompressed WAV are supported at a minimum.
    Depending on the implementation, other formats may be supported.

    """

    def __init__(self, fname, volume=100, balance=0, max_play=1):
        """Create a new sound object.

        ``fname`` indicates the name of the sound file, to be located in
        data/sounds.

        All remaining arguments set the initial properties of the sound.
        See Sound.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        pass

    def play(self, loops=0, maxtime=None, fade_time=None):
        """Play the sound.

        ``loops`` indicates the number of extra times to play the sound
        after it is played the first time; set to -1 or None to loop
        indefinitely.  ``maxtime`` indicates the maximum amount of time
        to play the sound in milliseconds; set to 0 or None for no
        limit. ``fade_time`` indicates the time in milliseconds over
        which to fade the sound in; set to 0 or None to immediately play
        the sound at full volume.

        """
        pass

    def stop(self, fade_time=None):
        """Stop the sound.

        ``fade_time`` indicates the time in milliseconds over which to
        fade the sound out before stopping; set to 0 or None to
        immediately stop the sound.

        """
        pass

    def pause(self):
        """Pause playback of the sound."""
        pass

    def unpause(self):
        """Resume playback of the sound if paused."""
        pass


class Music(object):

    """Music handling class.

    Music is mostly the same as sound, but only one can be played at a
    time.

    All Music objects have the following attributes:
        volume: The volume of the music in percent (0 for no sound, 100
            for max sound).
        balance: The balance of the music on stereo speakers.  A value
            of 0 means centered (an equal amount of play on both
            speakers), -1 means entirely in the left speaker, and 1
            means entirely in the right speaker.  Support for this
            feature in Stellar Game Engine implementations is optional.
            If it is unavailable, all music will be played through both
            speakers equally (assuming stereo sound is used).
        length: The length of the music in milliseconds.
        playing: Whether or not the music is playing.
        position: The current position (time) on the music in
            milliseconds.

    The following read-only attributes are also available:
        fname: The file name of the music given when it was created.
            See Music.__init__.__doc__ for more information.

    Music methods:
        Music.play: Play the music.
        Music.queue: Queue the music for playback.
        Music.stop: Stop the music.
        Music.pause: Pause playback of the music.
        Music.unpause: Resume playback of the music if paused.
        Music.restart: Restart music from the beginning.

    Ogg Vorbis is supported at a minimum.  Depending on the
    implementation, other formats may be supported.

    """

    def __init__(self, fname, volume=100, balance=0):
        """Create a new music object.

        ``fname`` indicates the name of the sound file, to be located in
        data/music.

        All remaining arguments set the initial properties of the music.
        See Music.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        pass

    def play(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Play the music.

        If music was already playing when this is called, it will be
        stopped.

        ``start`` indicates the number of milliseconds from the
        beginning to start at.  ``loops`` indicates the number of extra
        times to play the sound after it is played the first time; set
        to -1 or None to loop indefinitely.  ``maxtime`` indicates the
        maximum amount of time to play the sound in milliseconds; set to
        0 or None for no limit.  ``fade_time`` indicates the time in
        milliseconds over which to fade the sound in; set to 0 or None
        to immediately play the music at full volume.

        """
        pass

    def queue(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Queue the music for playback.

        This will cause the music to be added to a list of music to play
        in order, after the previous music has finished playing.

        See Music.play.__doc__ for information about the arguments.

        """
        pass

    def stop(self, fade_time=None):
        """Stop the music.

        ``fade_time`` indicates the time in milliseconds over which to
        fade the sound out before stopping; set to 0 or None to
        immediately stop the music.

        """
        pass

    def pause(self):
        """Pause playback of the music."""
        pass

    def unpause(self):
        """Resume playback of the music if paused."""
        pass


class StellarClass(object):

    """Class for game objects.

    All StellarClass objects have the following attributes:
        x: The horizontal position of the object in the room, where the
            left edge is 0 and x increases toward the right.
        y: The vertical position of the object in the room, where the
            top edge is 0 and y increases toward the bottom.
        z: The Z-axis position of the object in the room, which
            determines in what order objects are drawn; objects with a
            higher Z value are drawn in front of objects with a lower Z
            value.
        sprite: The sprite currently in use by this object.  Set to None
            for no (visible) sprite.  While it will always be an actual
            Sprite object or None when read, it can also be set to the
            ID of a sprite.
        visible: Whether or not the object should be drawn.
        detects_collisions: Whether or not the object should be involved
            in collisions.
        bbox_x: The horizontal location of the top-left corner of the
            bounding box in relation to x, where 0 is x and bbox_x
            increases toward the right.
        bbox_y: The vertical location of the top-left corner of the
            bounding box in relation to y, where 0 is y and bbox_y
            increases toward the bottom.
        bbox_width: The width of the bounding box in pixels.
        bbox_height: The height of the bounding box in pixels.
        collision_ellipse: Whether or not an ellipse (rather than a
            rectangle) should be used for collision detection.
        collision_precise: Whether or not precise (pixel-perfect)
            collision detection should be used.
        bbox_left: The position of the left side of the bounding box in
            the room (same as x + bbox_x).
        bbox_right: The position of the right side of the bounding box
            in the room (same as bbox_left + bbox_width).
        bbox_top: The position of the top side of the bounding box
            (same as y + bbox_y).
        bbox_bottom: The position of the bottom side of the bounding
            box (same as bbox_top + bbox_height).
        xvelocity: The velocity of the object toward the right.  Default
            is 0.
        yvelocity: The velocity of the object toward the bottom.
            Default is 0.
        speed: The total (directional) speed of the object.  Default is
            0.
        move_direction: The direction of the object's movement in
            degrees, with 0 being directly to the right and rotation in
            a positive direction being counter-clockwise.  Default is 0.
        image_index: The animation frame currently being displayed, with
            0 being the first one.  Default is 0.
        image_fps: The animation rate in frames per second.  Default is
            the value recommended by the sprite, or 0 if there is no
            sprite.
        image_xscale: The horizontal scale factor for the sprite.
            Default is 1.
        image_yscale: The vertical scale factor for the sprite.  Default
            is 1.
        image_rotation: The rotation of the sprite, with rotation in a
            positive direction being counter-clockwise.  Default is 0.
        image_alpha: The alpha value applied to the entire image, where
            255 is the original image, 128 is half the opacity of the
            original image, 0 is fully transparent, etc.  Default is
            255.
        image_blend: The color to blend with the sprite.  Set to None
            for no color blending.  Default is None.

    The following read-only attributes are also available:
        id: The unique identifier for this object.
        xstart: The initial value of x when the object was created.
        ystart: The initial value of y when the object was created.
        xprevious: The previous value of x.
        yprevious: The previous value of y.

    StellarClass methods:
        collides: Return whether or not this object collides with
            another.
        set_alarm: Set an alarm.
        destroy: Destroy the object.

    StellarClass events are handled by special methods.  The time that
    they are called is based on the following events, which happen each
    frame in the following order and are synchronized among all objects
    which have them:
        event_step_begin
        event_step
        event_step_end

    The following events are not timed in any particular way, but are
    called immediately when the engine detects them occurring:
        event_create
        event_animation_end
        event_destroy
        event_alarm

    The following events are always called (in no particular order)
    between calls of event_step and event_step_end:
        event_collision
        event_collision_left
        event_collision_right
        event_collision_top
        event_collision_bottom

    """

    def __init__(self, x, y, z, sprite=None, visible=True,
                 detects_collisions=True, bbox_x=None, bbox_y=None,
                 bbox_width=None, bbox_height=None, collision_ellipse=False,
                 collision_precise=False, id_=None, **kwargs):
        """Create a new StellarClass object.

        Arguments set the properties of the object.  See
        StellarClass.__doc__ for more information.

        If bbox_x, bbox_y, bbox_width, or bbox_height is None, the
        respective argument will be determined by the sprite's suggested
        bounding box.

        If ``id`` is None, it will be set to an integer not currently
        used as an ID (the exact number chosen is implementation-
        specific and may not necessarily be the same between runs).

        A game object must exist before an object of this class is
        created.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        if 'id' in kwargs:
            id_ = kwargs['id']

    def collides(self, other, x=None, y=None):
        """Return whether or not this object collides with another.

        ``other`` indicates the object to check for a collision with, or
        the name of said object.  ``other`` can also be a class to check
        for collisions with.

        ``x`` and ``y``, indicate the position to check for collisions
        at.  If unspecified or None, this object's current position will
        be used.

        """
        pass

    def set_alarm(self, alarm_id, value):
        """Set an alarm.

        Set the alarm with the given ``alarm_id`` with the given
        ``value``.  The alarm will then reduce by 1 each frame until it
        reaches 0 and set off the alarm event with the same ID.
        ``alarm_id`` can be any value.  ``value`` should be a number
        greater than 0.  You can also set ``value`` to None to disable
        the alarm.

        """
        pass

    def get_alarm(self, alarm_id):
        """Return the count on an alarm.

        Get the number of frames before the alarm with ``alarm_id`` will
        go off.  If the alarm has not been set, None will be returned.

        """
        pass

    def destroy(self):
        """Destroy the object."""
        pass

    def event_create(self):
        """Create event."""
        pass

    def event_animation_end(self):
        """Animation End event."""
        pass

    def event_destroy(self):
        """Destroy event."""
        pass

    def event_step_begin(self):
        """Begin Step event."""
        pass

    def event_alarm(self, alarm_id):
        """Alarm event.

        ``alarm_id`` is the ID of the alarm that was set off.

        """
        pass

    def event_step(self):
        """Step event."""
        pass

    def event_collision(self, other):
        """Middle/default collision event."""
        pass

    def event_collision_left(self, other):
        """Left collision event."""
        self.event_collision(other)

    def event_collision_right(self, other):
        """Right collision event."""
        self.event_collision(other)

    def event_collision_top(self, other):
        """Top collision event."""
        self.event_collision(other)

    def event_collision_bottom(self, other):
        """Bottom collision event."""
        self.event_collision(other)

    def event_step_end(self):
        """End step event."""
        pass


class Mouse(StellarClass):

    def event_collision(self, other):
        game.event_mouse_collision(other)

    def event_collision_left(self, other):
        game.event_mouse_collision_left(other)

    def event_collision_right(self, other):
        game.event_mouse_collision_right(other)

    def event_collision_top(self, other):
        game.event_mouse_collision_top(other)

    def event_collision_bottom(self, other):
        game.event_mouse_collision_bottom(other)


class Room(object):

    """Class for rooms.

    All Room objects have the following attributes:
        width: The width of the room in pixels.
        height: The height of the room in pixels.
        views: A list containing all View objects in the room.
        background: The Background object used.  While it will always be
            the actual object when read, it can be set to either an
            actual background object or the ID of a background.

    The following read-only attributes are also available:
        objects: A tuple containing all StellarClass objects in the
            room.
        room_number: The index of this room in the game, where 0 is the
            first room, or None if this room has not been added to a
            game.

    Room methods:
        add: Add a StellarClass object to the room.
        start: Start the room.
        resume: Continue the room from where it left off.
        end: Go to the next room.

    Room events are handled by special methods.  The following events
    happen each frame in the following order and are synchronized among
    all objects which have them:
        event_step_begin
        event_step
        event_step_end

    The following events are not timed in any particular way, but are
    called immediately when the engine detects them occurring:
        event_room_start
        event_room_end

    """

    def __init__(self, objects=(), width=DEFAULT_SCREENWIDTH,
                 height=DEFAULT_SCREENHEIGHT, views=None, background=None):
        """Create a new Room object.

        Arguments set the properties of the room.  See Room.__doc__ for
        more information.

        If ``views`` is set to None, a new view will be  created with
        x=0, y=0, and all other arguments unspecified, which will become
        the first view of the room.  If ``background`` is set to None, a
        new background is created with no layers and the color set to
        "black".

        In addition to containing actual StellarClass objects,
        ``objects`` can contain valid IDs of StellarClass objects.

        A game object must exist before an object of this class is
        created.

        """
        pass

    def add(self, obj):
        """Add a StellarClass object to the room.

        ``obj`` is the StellarClass object to add.  It can also be an
        object's ID.

        """
        pass

    def start(self):
        """Start the room.

        If the room has been changed, reset it to its original state.

        """
        pass

    def resume(self):
        """Continue the room from where it left off.

        If the room is unchanged (e.g. has not been started yet), this
        method behaves in the same way that Room.start does.

        """
        pass

    def end(self):
        """Start the next room.

        If this room is the last room, the game is ended.  Note that
        this does not reset the state of this room.  The state of the
        next room, if any, is reset, however.

        """
        pass

    def event_room_start(self):
        """Room start event."""
        pass

    def event_room_end(self):
        """Room end event."""
        pass

    def event_step_begin(self):
        """Room begin step event."""
        pass

    def event_step(self):
        """Room step event."""
        pass

    def event_step_end(self):
        """Room end step event."""
        pass


class View(object):

    """Class for room views.

    All View objects have the following attributes:
        x: The horizontal position of the view in the room, where the
            left edge is 0 and x increases toward the right.
        y: The vertical position of the view in the room, where the top
            edge is 0 and y increases toward the bottom.
        xport: The horizontal position of the view on the screen, where
            the left edge is 0 and xport increases toward the right.
        yport: The vertical position of the view on the screen, where
            the top edge is 0 and yport increases toward the bottom.
        width: The width of the view in pixels.
        height: The height of the view in pixels.

    """

    def __init__(self, x, y, xport=0, yport=0, width=None, height=None):
        """Create a new View object.

        Arguments set the properties of the view.  See View.__doc__ for
        more information.

        If ``width`` or ``height`` is set to None, the respective size
        will be set such that the view takes up all of the space that it
        can (i.e. game.width - xport or game.height - yport).

        """
        self.x = x
        self.y = y
        self.xport = xport
        self.yport = yport
        self.width = width if width else game.width - xport
        self.height = height if height else game.height - yport
