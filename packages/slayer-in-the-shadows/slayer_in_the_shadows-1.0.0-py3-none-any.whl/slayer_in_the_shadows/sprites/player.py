"""The player"""

from random import randint

import arcade

from ..assets import get_asset_path, get_sprite_path
from ..constants import (
    ANIMATION_FREEZE_TIME,
    DASH_COOLDOWN,
    INVULNERABILITY_DURATION,
    MAX_DASHES,
    SLOW_TIME_COOLDOWN,
    SLOW_TIME_DURATION,
)
from .attacks import player_attacks
from .bars import ChargeBar
from .character import Character


# pylint: disable=too-many-instance-attributes
class Player(Character):
    """The main player The player sprite is 32x26"""

    # pylint: disable=too-many-arguments
    def __init__(self, bottom, left, health: int, speed: int, game):
        super().__init__(bottom, left, None, health, speed, player_attacks, game, character_scaling=2)
        self.jump_index = None
        self.dashes = None
        self.dash_cooldown = None

        self.is_slowing_time = None
        self.slow_time_duration = None
        self.slow_time_cooldown = None

        self.is_facing_right = None
        self.is_on_ground = None
        self.force = None
        self.last_position = None

        self.is_charging_attack = None
        self.charge_duration = None

        with get_sprite_path("player", "idle") as sprite_path:
            self.idle = [[], []]
            for i in range(2):
                self.idle[i] = arcade.load_textures(
                    sprite_path,
                    [(j * 32, 0, 32, 26) for j in range(4)],
                    bool(i),
                    hit_box_algorithm="Detailed",
                )
            self.texture = self.idle[0][0]
        with get_sprite_path("player", "move") as sprite_path:
            self.move = [[], []]
            for i in range(2):
                self.move[i] = arcade.load_textures(
                    sprite_path,
                    [(j * 36, 0, 36, 26) for j in range(3)],
                    bool(i),
                    hit_box_algorithm="Detailed",
                )
        with get_sprite_path("player", "jump") as sprite_path:
            self.jump = [[], []]
            for i in range(2):
                self.jump[i] = arcade.load_textures(
                    sprite_path,
                    [(j * 34, 0, 34, 30) for j in range(8)],
                    bool(i),
                    hit_box_algorithm="Detailed",
                )

        self.bottom = bottom
        self.left = left

        with get_asset_path("sounds", "whoosh.wav") as soundfile:
            self.whoosh = arcade.load_sound(soundfile)

        self.charge_bar = ChargeBar(self)

    def setup_player(self):
        """Setup the player"""
        self.dashes = MAX_DASHES
        self.dash_cooldown = 0

        self.is_slowing_time = False
        self.slow_time_duration = 0
        self.slow_time_cooldown = 0

        self.is_facing_right = True
        self.is_on_ground = True
        self.force = (0, 0)
        self.jump_index = -1

        self.is_charging_attack = False
        self.charge_duration = 0

    def update_animation(self, delta_time: float = 1 / 60):
        """Update the animation"""
        if not self.jump_index >= 0:
            if self.is_on_ground:
                self.cur_texture_index += 1
                if self.cur_texture_index >= 4 * ANIMATION_FREEZE_TIME * 3:
                    self.cur_texture_index = 0
                if self.force == (0, 0):
                    self.texture = self.idle[int(not self.is_facing_right)][
                        self.cur_texture_index // (3 * ANIMATION_FREEZE_TIME)
                    ]
                else:
                    self.texture = self.move[int(not self.is_facing_right)][
                        self.cur_texture_index // (4 * ANIMATION_FREEZE_TIME)
                    ]
            else:
                self.texture = self.jump[int(not self.is_facing_right)][7]
        else:
            self.texture = self.jump[int(not self.is_facing_right)][self.jump_index // (ANIMATION_FREEZE_TIME + 3)]
            self.jump_index += 1
            if self.jump_index >= (ANIMATION_FREEZE_TIME + 3) * 5:
                self.jump_index = -1

    def use_dash(self):
        """
        Uses a dash
        Doesn't implement it, just adjusts player values
        """
        arcade.play_sound(self.whoosh, 0.5, speed=randint(100, 150) / 100)
        self.dashes -= 1
        self.dash_cooldown = DASH_COOLDOWN

    def slow_time(self):
        """
        Slows time
        Doesn't implement it, just adjusts player values
        """
        self.slow_time_duration = SLOW_TIME_DURATION
        self.is_slowing_time = True

    def update(self):
        """Updates player"""
        super().update()
        self.charge_bar.update()

    def on_update(self, delta_time: float = 1 / 60):
        """
        Time related cooldowns like attack and invulnerability
        """
        # Dash
        # If still on cooldown
        if self.dash_cooldown:
            self.dash_cooldown = max(self.dash_cooldown - delta_time, 0)
        # Not on cooldown
        elif self.dashes < MAX_DASHES:
            self.dashes += 1
            if self.dashes < MAX_DASHES:
                self.dash_cooldown = DASH_COOLDOWN

        # Time slow
        if self.is_slowing_time:
            if not self.slow_time_duration:
                self.is_slowing_time = False
                self.slow_time_cooldown = SLOW_TIME_COOLDOWN
            else:
                self.slow_time_duration = max(self.slow_time_duration - delta_time, 0)
        elif self.slow_time_cooldown:
            self.slow_time_cooldown = max(self.slow_time_cooldown - delta_time, 0)

        if self.is_charging_attack:
            self.charge_duration += delta_time

        super().on_update(delta_time)

    def take_damage(self, damage: int):
        """Handles damage taking"""
        if not self.is_invulnerable:
            self.health -= damage
            self.is_invulnerable = True
            self.invulnerable_duration = INVULNERABILITY_DURATION
            if self.health <= 0:
                self.game.setup()
                return
            self.health_bar.update_health()
