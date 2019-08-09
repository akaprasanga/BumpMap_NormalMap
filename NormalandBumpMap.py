import pyvips
import ntpath


class NormalAndBumpMap:

    def __init__(self, img_path, mode='normal_map', factor=1):

        self.img_path = img_path

        if mode == 'normal_map':
            self.normal_map(self.img_path, factor)

        elif mode == 'bump_map':
            self.bump_map(self.img_path, factor)

    def bump_map(self, filename, factor=1):
        names = [filename]*2
        gray = [pyvips.Image.new_from_file(filename, access='sequential').colourspace('b-w') / 255 for filename in names]

        move_right = gray[0].wrap(x=factor, y=0)
        move_left = gray[0].wrap(x=-factor, y=0)
        move_up = gray[1].wrap(x=0, y=factor)
        move_down = gray[1].wrap(x=0, y=-factor)

        dx = move_right.subtract(move_left)
        dy = move_up.subtract(move_down)

        denominator = (dx * dx + dy * dy + 1) ** 0.5

        nx = (-dx).divide(denominator)
        ny = (-dy).divide(denominator)
        nz = (1 / denominator)

        r_cal = ((nx + 1).divide(2)).multiply(255)
        g_cal = ((ny + 1).divide(2)).multiply(255)
        b_cal = nz.multiply(255)

        bump = (r_cal * 0.2126 + g_cal * 0.7152 + b_cal * 0.0722).cast('uchar')
        bump.write_to_file(ntpath.basename(filename)+"_bump.jpg")
        return bump

    def normal_map(self, filename, factor=1):
        names = [filename, filename]
        gray = [pyvips.Image.new_from_file(filename, access='random') / 255 for filename in names]

        bands = gray[0].bandsplit()
        band_sum = bands[0] + bands[1] + bands[2]
        ready_img = 0.9*band_sum
        gray[0] = ready_img
        gray[1] = ready_img

        move_right = gray[0].wrap(x=factor, y=0)
        move_left = gray[0].wrap(x=-factor, y=0)
        move_up = gray[1].wrap(x=0, y=factor)
        move_down = gray[1].wrap(x=0, y=-factor)

        dx = move_right.subtract(move_left)
        dy = move_up.subtract(move_down)

        denominator = (dx * dx + dy * dy + 1) ** 0.5

        nx = (-dx).divide(denominator)
        ny = (-dy).divide(denominator)
        nz = (1 / denominator)

        r_cal = ((nx + 1).divide(2)).multiply(255)
        g_cal = ((ny + 1).divide(2)).multiply(255)
        b_cal = nz.multiply(255)

        normal = r_cal.bandjoin([g_cal, b_cal])
        normal.write_to_file(ntpath.basename(filename)+"_normal.jpg")


if __name__ == "__main__":
    img_path = "path_to_image"
    mapObj = NormalAndBumpMap(img_path=img_path, mode='normal_map', factor=1)

