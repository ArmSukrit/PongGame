from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.label import Label


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player_red = ObjectProperty(None)
    player_blue = ObjectProperty(None)
    decisive_points = 3  # end the game when a player reaches this point

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player_red.bounce_ball(self.ball)
        self.player_blue.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player_blue.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player_red.score += 1
            self.serve_ball(vel=(-4, 0))

        # check if game ends
        if self.player_red.score == self.decisive_points:
            self.pause_at_game_end("red")
        if self.player_blue.score == self.decisive_points:
            self.pause_at_game_end("blue")

    def pause_at_game_end(self, winner):
        self.clear_points()

    def clear_points(self):
        self.player_blue.score = 0
        self.player_red.score = 0

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player_red.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player_blue.center_y = touch.y


# class EndSc
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
