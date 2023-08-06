
import click
import os
from PIL import Image


def crommakey(value:int, tolerance:int, match_value:int)->bool:
	if (value-tolerance) >= 0:
		l_value = value - tolerance
	else:
		l_value = 0

	if (value+tolerance) <= 255:
		u_value = value + tolerance
	else:
		u_value = 255

	if match_value <= u_value and match_value >= l_value:
		return True
	else:
		return False


@click.command(
        help="Adds background to any transparent image"
        )
@click.option(
        '-i', 
        '--inputimage', 
        type=click.Path(),
        default="./main.png",
        show_default=True,
        help="Front Image"
        )
@click.option(
        '-o', 
        '--outputimage', 
        type=click.Path(),
        default="./main_removedbg.png",
        show_default=True,
        help="Resized output image"
        )
@click.option(
		'-c',
		'--color',
		type=click.Tuple([int, int, int]),
		default=(255, 255, 255),
		show_default=True,
		help="Color to be removed"
		)
@click.option(
		'-C',
		'--color_with',
		type=click.Tuple([int, int, int]),
		default=(255, 255, 255),
		show_default=True,
		help="Color to replace with."
		)
def replace(inputimage, outputimage, color, color_with):
	inputimage = Image.open(inputimage)
	img = inputimage.convert("RGBA")
	datas = img.getdata()
	newData = []

	for item in datas:
		if item[0] == color[0] and item[1] == color[1] and item[2] == color[2]:
			newData.append((color_with[0], color_with[1], color_with[2], 255))
		else:
			newData.append(item)

	img.putdata(newData)
	img.save(outputimage, "PNG")
	click.echo(f'{inputimage} is processed as {outputimage}.')





