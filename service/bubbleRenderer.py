import sys
import drawsvg
import circlify as circ
import random
import math as m
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QImage, QPainter
from PySide6.QtCore import QXmlStreamReader
from PySide6.QtWidgets import QApplication


def sin(phi):
    """ calculactes sin value from degree"""
    return m.sin(phi * m.pi / 180)


def cos(phi):
    """ calculactes cos value from degree"""
    return m.cos(phi * m.pi / 180)


def radius(x, y):
    """calculates radius from x and y"""
    return m.sqrt(x ** 2 + y ** 2)


class BubbleRenderer:
    packings = ['circle', 'rectangle', 'planets']

    def __init__(self, **kwargs):
        self.frame = None
        self.size = None
        self.data = None
        self.labels = None
        self.cmap = None
        self.dpi: int = 600
        self.packing = None
        self.background_color = None
        self.file = None
        self.png = False
        self.resolution: int = None
        self.gradient: bool = True
        self.gradient_stops: list = [0, 20, 80, 100]
        self.stroke: bool = False
        self.stroke_color: str = 'black'
        self.stroke_width: int = 1
        self.text_color: str = 'black'
        self.text_size: int = 10
        self.text_anchor: str = 'middle'
        self._parse_kwargs(kwargs)

    def render(self):
        self._create_frame()
        self._create_bubbles()
        quit = False
        if self.png:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
                quit = True
            reader = QXmlStreamReader()
            reader.addData(self.frame.as_svg())
            renderer = QSvgRenderer()
            renderer.load(reader)
            img = QImage(self.size[0], self.size[1], QImage.Format_ARGB32)
            painter = QPainter(img)
            renderer.render(painter)
            img.save(self.file)
            painter.end()
            if quit:
                app.quit()
        elif self.file:
            self.frame.save_svg(self.file)
        return self.frame

    def _create_frame(self):
        """Create a frame for the bubble chart"""
        if self.size is None:
            raise ValueError("Size is not set")
        elif int(self.size[0]) < 0 or int(self.size[1]) < 0:
            raise ValueError("Size must be positive")
        self.frame = drawsvg.Drawing(
            width=self.size[0],
            height=self.size[1],
            origin='center',
            style=f"background-color: " + str(self.background_color),
        )

    def _create_bubbles(self):
        circles = []
        datasum: float = sum(self.data)
        combined_data_labels = list(zip(self.data, self.labels))
        sorted_combined = sorted(combined_data_labels, key=lambda x: x[0], reverse=True)
        sorted_data, sorted_labels = zip(*sorted_combined)
        print(f"unsorted date={list(zip(self.data, self.labels))}")
        print(f"{sorted_combined =}")
        if self.packing == 'circle':
            circles = circ.circlify(
                sorted_data,
                target_enclosure=circ.Circle(x=0, y=0, r=self.size[0] / 2),
                show_enclosure=False,
            )
            circles = sorted(circles, key=lambda x: x.r, reverse=True)
        elif self.packing == 'rectangle':
            pass
        elif self.packing == 'planets':
            dPhi = 360 / len(sorted_data)
            Phi = [i * dPhi for i in range(len(sorted_data) - 1)]
            initial_radius = self.size[0] / 10
            for i, data in enumerate(sorted_data):
                if i == 0:
                    circles.append(circ.Circle(x=0, y=0, r=initial_radius))  # Sun data point
                    continue
                r = (sorted_data[i] / sorted_data[0]) * initial_radius  # Planet radius
                # polar coordinates
                R = radius(circles[i - 1].x, circles[i - 1].y) + circles[i - 1].r + r
                phi = Phi.pop(0) if i % 2 == 0 else Phi.pop(int(len(Phi) / 2))
                R = self.fit_R(R, phi, r, circles)
                circle = circ.Circle(x=R * cos(phi), y=R * sin(phi), r=r)
                circles.append(circle)
        # calculate color gradient and add circles to the frame
        if circles is None:
            raise ValueError("Circles could not be created")
        for i, circle in enumerate(circles):
            x = circle.x
            y = circle.y
            r = 0.8 * circle.r
            first_gradient = drawsvg.RadialGradient(
                cx=x,
                cy=y,
                r=r,
                fx=x,
                fy=y,
            )
            first_gradient.add_stop(offset=f"{self.gradient_stops[0]}%", color=self.cmap[1])
            first_gradient.add_stop(offset=f"{self.gradient_stops[1]}%", color=self.cmap[1])
            first_gradient.add_stop(offset=f"{self.gradient_stops[2]}%", color=self.cmap[0])
            first_gradient.add_stop(offset=f"{self.gradient_stops[3]}%", color=self.background_color)
            self.frame.append(drawsvg.Circle(
                cx=x,
                cy=y,
                r=r,
                fill=first_gradient,
                stroke=self.stroke_color if self.stroke else 'none',
                stroke_width=self.stroke_width,
            ))
            self.frame.append(drawsvg.Text(
                text=f"""{sorted_labels[i]}""",
                x=x,
                y=y - self.text_size,
                text_anchor=self.text_anchor,
                font_size=self.text_size,
                fill=self.text_color,
            ))
            self.frame.append(drawsvg.Text(
                text=f"""{sorted_data[i]}""",
                x=x,
                y=y,
                text_anchor=self.text_anchor,
                font_size=self.text_size,
                fill=self.text_color,
            ))
            self.frame.append(drawsvg.Text(
                text=f"""{sorted_data[i] / datasum * 100:.2f}%""",
                x=x,
                y=y + self.text_size,
                text_anchor=self.text_anchor,
                font_size=self.text_size,
                fill=self.text_color,
            ))

    def _create_random_data(self):
        """Create random data for testing"""
        self.data = [random.randint(1, 500) for _ in range(20)]
        self.labels = [f"Label {i}" for i in range(20)]

    def _parse_kwargs(self, kwargs):
        """Parse keyword arguments"""
        if 'size' in kwargs:
            self.size = kwargs['size']
        else:
            self.size = (500, 500)
        if 'data' in kwargs:
            self.data = kwargs['data']
        else:
            self._create_random_data()
        if 'labels' in kwargs:
            self.labels = kwargs['labels']
        if 'cmap' in kwargs:
            self.cmap = kwargs['cmap']
        if  'gradient_stops' in kwargs:
            self.gradient_stops = kwargs['gradient_stops']
        if 'background_color' in kwargs:
            self.background_color = kwargs['background_color']
        if 'text_size' in kwargs:
            self.text_size = kwargs['text_size']
        if 'text_color' in kwargs:
            self.text_color = kwargs['text_color']
        if 'text_anchor' in kwargs:
            self.text_anchor = kwargs['text_anchor']
        if 'stroke' in kwargs:
            self.stroke = kwargs['stroke']
        if 'stroke_color' in kwargs:
            self.stroke_color = kwargs['stroke_color']
        if 'stroke_width' in kwargs:
            self.stroke_width = kwargs['stroke_width']
        if 'packing' in kwargs:
            if kwargs['packing'] not in self.packings:
                raise ValueError(f"'packing' must be one of the following: {self.packings!s}")
            self.packing = kwargs['packing']
        if 'png' in kwargs and 'file' in kwargs:
            self.png = kwargs['png']
            self.file = kwargs['file']
        elif 'png' in kwargs and 'file' not in kwargs:
            raise ValueError("File name is not set")

    def fit_R(self, R, phi, r, circles):
        d_r = 10
        collided = False
        while not collided:
            x = R * cos(phi)
            y = R * sin(phi)
            for i, circle in enumerate(circles):
                distance = radius(x - circle.x, y - circle.y)
                min_distance = circle.r + r
                if distance <= min_distance:
                    collided = True
                    return R
            R -= d_r


if __name__ == "__main__":
    br = BubbleRenderer(
        size=(3000, 3000),
        background_color='white',
        cmap=[
            '#C2185B',
            '#FCE4EC'],
        packing='circle',
        png=True,
        file="bubbles.png"
    )
    br.text_size = 50
    br.gradient_stops = [0, 50, 90, 100]
    img = br.render()
    img.save_svg("bubble.svg")
